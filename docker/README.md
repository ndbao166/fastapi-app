# Docker Setup Guide

Hướng dẫn chi tiết về cách build và run Docker container cho dự án FastAPI với uv package manager.

## 📋 Mục lục

- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Build Docker Image](#build-docker-image)
- [Run Docker Container](#run-docker-container)
- [Docker Compose](#docker-compose)
- [Các lệnh hữu ích](#các-lệnh-hữu-ích)
- [Troubleshooting](#troubleshooting)

## 🔧 Yêu cầu hệ thống

- Docker version 20.0+ 
- Docker Compose version 2.0+
- Git

Kiểm tra phiên bản Docker:
```bash
docker --version
docker-compose --version
```

## 📁 Cấu trúc dự án

```
fastapi-cicd-lint-mypy-uv/
├── docker/
│   ├── backend/
│   │   └── Dockerfile          # Dockerfile cho backend
│   ├── frontend/
│   └── README.md              # File hướng dẫn này
├── src/
│   └── main.py                # Ứng dụng chính
├── pyproject.toml             # Cấu hình dự án và dependencies
├── uv.lock                    # Lock file cho uv
├── makefile                   # Makefile với các lệnh phổ biến
└── docker-compose.yml         # Docker compose configuration
```

## 🐳 Build Docker Image

### 1. Build từ thư mục gốc

```bash
# Di chuyển đến thư mục gốc của dự án
cd /home/bao/learn/fastapi-cicd-lint-mypy-uv

# Build image với tag tùy chỉnh
docker build -f docker/backend/Dockerfile -t fastapi-app:latest .
```

### 2. Build với các tham số bổ sung

```bash
# Build với cache bỏ qua
docker build --no-cache -f docker/backend/Dockerfile -t fastapi-app:latest .

# Build với build arguments (nếu cần)
docker build --build-arg PYTHON_VERSION=3.10 -f docker/backend/Dockerfile -t fastapi-app:latest .

# Build và gắn thêm tag
docker build -f docker/backend/Dockerfile -t fastapi-app:latest -t fastapi-app:v1.0.0 .
```

### 3. Xem thông tin image đã build

```bash
# Liệt kê các images
docker images

# Xem chi tiết image
docker inspect fastapi-app:latest

# Xem lịch sử build layers
docker history fastapi-app:latest
```

## 🚀 Run Docker Container

### 1. Chạy container cơ bản

```bash
# Chạy container
docker run --name fastapi-container fastapi-app:latest

# Chạy container ở background (detached mode)
docker run -d --name fastapi-container fastapi-app:latest

# Chạy container với port mapping (nếu app có web server)
docker run -d -p 8000:8000 --name fastapi-container fastapi-app:latest
```

### 2. Chạy với các tham số bổ sung

```bash
# Chạy với volume mount để sync code
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  -v $(pwd)/src:/app/src \
  fastapi-app:latest

# Chạy với environment variables
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  -e ENV=development \
  -e DEBUG=true \
  fastapi-app:latest

# Chạy với resource limits
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  --memory=512m \
  --cpus=1.0 \
  fastapi-app:latest
```

### 3. Chạy interactive mode

```bash
# Chạy container với interactive terminal
docker run -it --name fastapi-container fastapi-app:latest /bin/bash

# Override command để debug
docker run -it --name fastapi-container fastapi-app:latest /bin/bash

# Chạy một lệnh cụ thể trong container
docker run --rm fastapi-app:latest uv run --help
```

## 🔄 Docker Compose

Nếu có file `docker-compose.yml`, bạn có thể sử dụng:

```bash
# Build và run với docker-compose
docker-compose up --build

# Chạy ở background
docker-compose up -d --build

# Chỉ build không run
docker-compose build

# Stop và remove containers
docker-compose down

# Stop, remove containers và volumes
docker-compose down -v
```

## 🛠 Các lệnh hữu ích

### Quản lý containers

```bash
# Xem containers đang chạy
docker ps

# Xem tất cả containers (cả stopped)
docker ps -a

# Stop container
docker stop fastapi-container

# Start container đã stop
docker start fastapi-container

# Restart container
docker restart fastapi-container

# Remove container
docker rm fastapi-container

# Remove container khi stop (auto cleanup)
docker run --rm --name fastapi-container fastapi-app:latest
```

### Debug và monitoring

```bash
# Xem logs container
docker logs fastapi-container

# Follow logs real-time
docker logs -f fastapi-container

# Xem logs với timestamp
docker logs -t fastapi-container

# Exec vào container đang chạy
docker exec -it fastapi-container /bin/bash

# Xem resource usage
docker stats fastapi-container

# Xem processes trong container
docker top fastapi-container
```

### Quản lý images

```bash
# Xem danh sách images
docker images

# Remove image
docker rmi fastapi-app:latest

# Remove tất cả unused images
docker image prune

# Remove tất cả images, containers, volumes
docker system prune -a
```

## 🎯 Dockerfile giải thích

File `docker/backend/Dockerfile` hiện tại:

```dockerfile
# Sử dụng base image với uv pre-installed
FROM python3.10-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy toàn bộ source code vào container
ADD . /app

# Set working directory
WORKDIR /app

# Sync dependencies từ uv.lock
RUN uv sync --locked

# Chạy ứng dụng bằng make command
CMD ["make", "run"]
```

### Các cờ (flags) quan trọng:

- `--locked`: Đảm bảo sync chính xác theo uv.lock file
- `python3.10-slim-trixie`: Base image nhẹ với Python 3.10
- `COPY --from=`: Multi-stage build để copy uv binary

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **Port already in use**
   ```bash
   # Tìm process đang sử dụng port
   lsof -i :8000
   
   # Hoặc sử dụng port khác
   docker run -p 8001:8000 fastapi-app:latest
   ```

2. **Container exits immediately**
   ```bash
   # Xem logs để debug
   docker logs fastapi-container
   
   # Chạy interactive để debug
   docker run -it fastapi-app:latest /bin/bash
   ```

3. **Build fails**
   ```bash
   # Build với verbose output
   docker build --progress=plain -f docker/backend/Dockerfile .
   
   # Clear build cache
   docker builder prune
   ```

4. **Permission denied**
   ```bash
   # Chạy với user mapping
   docker run -u $(id -u):$(id -g) fastapi-app:latest
   ```

### Tips optimization:

1. **Sử dụng .dockerignore**
   ```bash
   # Tạo file .dockerignore để loại trừ files không cần thiết
   echo "__pycache__" >> .dockerignore
   echo "*.pyc" >> .dockerignore
   echo ".git" >> .dockerignore
   ```

2. **Multi-stage builds**
   - Tách build stage và runtime stage
   - Giảm kích thước image cuối cùng

3. **Layer caching**
   - Copy requirements trước, code sau
   - Tận dụng Docker layer cache

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs: `docker logs <container_name>`
2. Exec vào container: `docker exec -it <container_name> /bin/bash`
3. Kiểm tra network: `docker network ls`
4. Kiểm tra volumes: `docker volume ls`

---

**Lưu ý**: File này được tạo tự động. Cập nhật theo nhu cầu dự án cụ thể.
