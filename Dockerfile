FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 预下载 Chroma 默认使用的文本嵌入模型（固化到镜像）
RUN python -c "from chromadb.utils import embedding_functions; embedding_functions.DefaultEmbeddingFunction()"

# 复制应用代码
COPY streamlit_app.py .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]