FROM python:3.12-slim

WORKDIR /app

# 安装依赖（GitHub Actions 在美国，用 PyPI 官方源更快）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 预下载嵌入模型
RUN python -c "from chromadb.utils import embedding_functions; embedding_functions.DefaultEmbeddingFunction()" 2>/dev/null || true

# 复制应用代码
COPY streamlit_app.py .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]