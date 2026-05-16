import sys
from openai import OpenAI

# 1. 先检查钥匙是不是真的换了（如果还是示范文字，立刻报警）
client = OpenAI(
    api_key="sk-69d3c258f03a4ae99d8bea3fc8eeda7a",   # <--- 拜托，一定要换成你从DeepSeek官网复制的那一长串
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