from ultralytics import YOLO

# Tải mô hình YOLO
model = YOLO('./app1/models/best.pt')


# Lưu mô hình đã chỉnh sửa vào file mới
model.export(format="torchscript", imgsz=640, dynamic=False, simplify=False, half=False)

print("Mô hình đã được lưu thành công.")