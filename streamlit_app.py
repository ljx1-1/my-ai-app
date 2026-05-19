import os
import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

# 从 Streamlit Secrets 或环境变量读取密钥
try:
    DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
except Exception:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

st.set_page_config(page_title="智能文档问答", page_icon="📄")
st.title("📄 文档智能问答系统")
st.caption("上传一份 PDF（合同、论文、说明书），直接对它提问")

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# 用 Chroma 自带的免费本地嵌入模型，不花钱不联网
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# 初始化或加载向量数据库（缓存起来，别每次都重做）
@st.cache_resource
def get_vector_db():
    return chromadb.PersistentClient(path="./chroma_db")

chroma_client = get_vector_db()
collection = chroma_client.get_or_create_collection(
    name="pdf_docs",
    embedding_function=embedding_function
)

# 上传 PDF
uploaded_file = st.file_uploader("上传 PDF 文件", type="pdf")

if uploaded_file is not None:
    # 读取 PDF 全部文本
    pdf = PdfReader(uploaded_file)
    full_text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

    if not full_text.strip():
        st.error("这个 PDF 好像没有文字（可能是扫描件），换个文档试试。")
    else:
        st.success(f"已读取文档，共 {len(full_text)} 个字符。")

        # 把文本切成小块，每块约 500 字，重叠 100 字
        chunk_size = 500
        overlap = 100
        chunks = []
        start = 0
        while start < len(full_text):
            end = start + chunk_size
            chunks.append(full_text[start:end])
            start = end - overlap
        st.info(f"文档已切成 {len(chunks)} 个片段，准备就绪。")

        # 获取当前库中的ID
        existing_ids = collection.get()["ids"]
        doc_name = uploaded_file.name

        # 如果库中没有这个文档，就存入
        if not any(doc_name in id for id in existing_ids):
            # 如果库非空，先清空（简单策略：每次只保留最新上传的一份文档）
            if existing_ids:
                collection.delete(ids=existing_ids)
            collection.add(
                documents=chunks,
                ids=[f"{doc_name}_{i}" for i in range(len(chunks))]
            )
            st.success("文档已索引，可以开始提问了！")
        else:
            st.info("文档已在库中，直接提问吧。")

        # 问答交互
        st.divider()
        query = st.text_input("你想问这份文档什么问题？", placeholder="例如：这份合同的违约责任是怎么约定的？")

        if query:
            with st.spinner("正在从文档中检索答案..."):
                # 从向量数据库检索最相关的3个片段
                results = collection.query(
                    query_texts=[query],
                    n_results=3
                )
                retrieved_docs = results["documents"][0] if results["documents"] else []
                context = "\n\n".join(retrieved_docs)

            if not context.strip():
                st.warning("没有找到相关段落，请换个问法试试。")
            else:
                with st.spinner("AI 正在结合原文生成回答..."):
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {
                                "role": "system",
                                "content": "你是一个严谨的文档助手。请严格根据下面提供的文档片段回答问题。如果片段中没有明确信息，就说‘文档中未提及’。禁止编造。\n\n【文档片段】\n" + context
                            },
                            {
                                "role": "user",
                                "content": query
                            }
                        ],
                        stream=False,
                        temperature=0.1
                    )
                    answer = response.choices[0].message.content

                st.markdown("### 🤖 AI 回答")
                st.success(answer)

                with st.expander("🔍 查看用来回答的原文片段（共3段）"):
                    for i, doc in enumerate(retrieved_docs):
                        st.markdown(f"**片段 {i+1}**: {doc}")
else:
    st.info("👆 上传一份 PDF，就可以开始提问啦。")