FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv（快速的 Python 包管理器）
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY backend/requirements.txt /app/backend/requirements.txt

# 安装 Python 依赖
RUN uv pip install --system -r backend/requirements.txt

# 复制项目文件
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
COPY scripts/ /app/scripts/

# 创建数据目录（用于持久化数据库）
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000

# 启动命令
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
