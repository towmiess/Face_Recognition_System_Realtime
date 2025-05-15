import cv2
import base64
import websockets
import asyncio
import json
from ultralytics import YOLO  # Import YOLO để sử dụng mô hình mới

# Tải mô hình YOLO mới
model = YOLO('./app1/models/updated_best.pt')  # Đường dẫn tới mô hình mới

async def send_frame():
    async with websockets.connect("ws/video_stream/") as ws:
        cap = cv2.VideoCapture(0)  # Sử dụng webcam

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Không thể đọc khung hình từ webcam.")
                break

            # Dự đoán đối tượng trong khung hình
            results = model(frame)

            # Chuyển đổi kết quả sang định dạng JSON
            detections = results.pandas().xyxy[0].to_json(orient="records")

            # Gửi kết quả qua WebSocket
            await ws.send(detections)
            response = await ws.recv()  # Nhận phản hồi từ server

            print(json.loads(response))  # Kiểm tra các đối tượng nhận diện được

asyncio.run(send_frame())