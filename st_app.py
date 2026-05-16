import streamlit as st
from openai import OpenAI

# 替换！
client = OpenAI(
    api_key="sk-69d3c258f03a4ae99d8bea3fc8eeda7a", 
    base_url="https://api.deepseek.com"
)

st.title("AI 起名大师")

# 用户输入
user_input = st.text_input("随便给个词，我给你起个花名", "小猫")

if st.button("起名！"):
    with st.spinner("正在翻字典..."):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个起名专家。收到一个词，就给用户编造一个五字以内的花名，并简单解释一下。不讲废话。"},
                {"role": "user", "content": user_input}
            ],
            stream=False
        )
        st.success(response.choices[0].message.content)