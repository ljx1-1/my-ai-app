# 智能文档问答系统 (PDF Q&A)

基于 Streamlit + DeepSeek + ChromaDB 的 RAG 文档问答应用。

上传一份 PDF（合同、论文、说明书），系统自动提取文本、建立向量索引，你可以直接用自然语言对文档内容提问，AI 会结合原文片段给出回答。

## 功能

- PDF 文本自动提取（支持多页）
- 文本分块 + 向量化存入 ChromaDB
- 提问时检索最相关的 3 个原文片段
- DeepSeek 大模型基于检索片段生成回答（严格不编造）
- 一键 Docker 部署

## 项目结构

```
├── streamlit_app.py    # 主应用：文档上传 + 问答
├── st_app.py        # 小工具：AI 起名
├── simple_ai.py     # 命令行测试：DeepSeek API 连通性
├── requirements.txt # Python 依赖
├── Dockerfile       # Docker 部署配置
├── chroma_db/       # 向量数据库本地持久化目录
└── start.sh         # 启动脚本
```

## 安装与运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API 密钥（Windows CMD 用 set，PowerShell 用 $env:）
export DEEPSEEK_API_KEY="你的DeepSeek密钥"

# 3. 启动应用
streamlit run streamlit_app.py
```

打开浏览器访问 `http://localhost:8501`。

## Docker 部署

```bash
docker build -t pdf-qa-app .
docker run -p 8501:8501 -e DEEPSEEK_API_KEY="你的密钥" pdf-qa-app
```

## 技术栈

| 组件 | 用途 |
|------|------|
| Streamlit | Web 界面 |
| pypdf | PDF 文本提取 |
| ChromaDB | 向量存储与相似度检索 |
| sentence-transformers | 文本嵌入模型 |
| DeepSeek API | 大语言模型生成回答 |
