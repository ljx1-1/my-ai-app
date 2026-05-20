FROM python:3.12-slim

WORKDIR /app

# 安装依赖（GitHub Actions 在美国，用 PyPI 官方源更快）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 预下载 Chroma 嵌入模型（79MB，运行时下载太慢，固化到镜像）
COPY download_model.py /tmp/
RUN python /tmp/download_model.py && rm /tmp/download_model.py

# 复制应用代码
COPY streamlit_app.py .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]