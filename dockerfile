# filepath: d:\study\XLA\BTL\RealTime-Face-Recognition-Attendance-System-for-Employees\dockerfile
FROM python:3.10-slim

WORKDIR /app

# Cài thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libboost-all-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục tạm
ENV TMPDIR=/app/tmp
RUN mkdir -p /app/tmp

# Copy và cài dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --cache-dir=/app/.pip-cache

# Copy toàn bộ mã nguồn
COPY . .

# Collect static nếu là Django
RUN python manage.py collectstatic --noinput || true

# Chạy ASGI app (FastAPI/Django Channels)
CMD ["uvicorn", "Project101.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
