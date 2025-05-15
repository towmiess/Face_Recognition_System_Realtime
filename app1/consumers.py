
import base64
import json
import cv2
import torch
import pygame
from channels.generic.websocket import AsyncWebsocketConsumer
from ultralytics import YOLO
import asyncio
from collections import deque
import numpy as np
import time  # Import time module for tracking duration

# Confidence threshold for detections
CONFIDENCE_THRESHOLD = 0.3  

# Global model & video capture (shared for all connections)
model = YOLO('app1/models/best.pt')  # Load YOLO model once
video_capture = cv2.VideoCapture(0)  # Shared video capture
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video_capture.set(cv2.CAP_PROP_FPS, 30)  # Adjust FPS to balance performance

# Initialize pygame for sound alerts
pygame.mixer.init()
alert_sound = pygame.mixer.Sound("app1/alert.mp3")  # Load alert sound file


class VideoStreamConsumer(AsyncWebsocketConsumer):
    active_connections = set()
    current_class_ids = []
    tracked_objects = {}
    object_entry_time = {}
    object_counter = 0
    ALERT_TIME_THRESHOLD = 3  # Seconds

    async def connect(self):
        print("WebSocket connected")
        self.active_connections.add(self)
        await self.accept()
        
        if len(self.active_connections) == 1:
            asyncio.create_task(self.stream_video())

    async def disconnect(self, close_code):
        print("WebSocket disconnected")
        self.active_connections.discard(self)
        
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('action') == 'set_class_ids':
            self.current_class_ids = data.get('class_ids', [])
            print(f"Class IDs set to {self.current_class_ids}")

        elif data.get('action') == 'set_confidence_threshold':
            new_threshold = data.get('confidence_threshold')
            if isinstance(new_threshold, (int, float)) and 0 <= new_threshold <= 1:
                global CONFIDENCE_THRESHOLD
                CONFIDENCE_THRESHOLD = new_threshold
                print(f"Confidence threshold set to {CONFIDENCE_THRESHOLD}")

    def calculate_iou(self, box1, box2):
        x1, y1, x2, y2 = box1
        x1_b, y1_b, x2_b, y2_b = box2

        inter_x1 = max(x1, x1_b)
        inter_y1 = max(y1, y1_b)
        inter_x2 = min(x2, x2_b)
        inter_y2 = min(y2, y2_b)

        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

        area1 = (x2 - x1) * (y2 - y1)
        area2 = (x2_b - x1_b) * (y2_b - y1_b)

        union_area = area1 + area2 - inter_area
        return inter_area / union_area if union_area != 0 else 0

    async def assign_tracking_ids(self, results, frame_id):
        detections = []
        current_time = time.time()

        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            confidence = result.conf[0].item()
            class_id = int(result.cls[0].item())

            if confidence > CONFIDENCE_THRESHOLD and (not self.current_class_ids or class_id in self.current_class_ids):
                detection = {
                    'bbox': (x1, y1, x2, y2),
                    'confidence': confidence,
                    'class_id': class_id,
                    'class_name': model.names[class_id]
                }

                assigned = False
                for track_id, tracked_data in list(self.tracked_objects.items()):
                    tracked_bbox = tracked_data[-1][1]
                    iou = self.calculate_iou(detection['bbox'], tracked_bbox)

                    if iou > 0.3:
                        self.tracked_objects[track_id].append((frame_id, detection['bbox']))
                        detection['track_id'] = track_id
                        assigned = True
                        break

                if not assigned:
                    self.object_counter += 1
                    track_id = self.object_counter
                    self.tracked_objects[track_id] = deque([(frame_id, detection['bbox'])])
                    detection['track_id'] = track_id

                if class_id in [1, 2]:
                    if track_id not in self.object_entry_time:
                        self.object_entry_time[track_id] = current_time
                    else:
                        duration = current_time - self.object_entry_time[track_id]
                        if duration > self.ALERT_TIME_THRESHOLD:
                            alert_message = {
                                "alert": f"Alert! Class ID {class_id}, Track ID {track_id} detected for {duration:.2f} seconds!",
                                "track_id": track_id,
                                "class_id": class_id,
                                "duration": round(duration, 2)
                            }
                            await self.send(text_data=json.dumps(alert_message))
                            pygame.mixer.Sound.play(alert_sound)
                            del self.object_entry_time[track_id]

                detections.append(detection)

        return detections

    async def stream_video(self):
        frame_id = 0
        while self.active_connections:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            results = model(frame, verbose=False)
            detections = await self.assign_tracking_ids(results, frame_id)

            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                label = f"{detection['class_name']}:{detection['confidence']:.2f} ID:{detection['track_id']}"
                # we need to change class id to show red rectanle
                color = (0, 0, 255) if detection['class_id'] in [1, 2] else (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')

            message = json.dumps({
                'frame': frame_data,
                'detected_objects': detections
            })

            tasks = [connection.send(text_data=message) for connection in self.active_connections]
            await asyncio.gather(*tasks, return_exceptions=True)

            await asyncio.sleep(0.02)
            frame_id += 1

        print("Video stream ended")
    