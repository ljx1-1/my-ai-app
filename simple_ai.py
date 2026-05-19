import os
import sys
from openai import OpenAI

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

print("🚀 开始请求DeepSeek...")

try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个幽默的助手"},
            {"role": "user", "content": "嗨，能讲个程序员才懂的笑话吗？"},
        ],
        stream=False
    )
    print("✅ 请求成功！AI回复：")
    print(response.choices[0].message.content)

except Exception as e:
    # 任何风吹草动都打印出来
    print("❌ 出错了！错误信息如下，请复制全段发给我：")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误详情: {str(e)}")
    sys.exit(1)