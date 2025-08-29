import requests
import json

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",  # Замените на ваш ключ
        "Content-Type": "application/json",
        # "HTTP-Referer": "<YOUR_SITE_URL>",
        # "X-Title": "<YOUR_SITE_NAME>",
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Hello! Tell me about yourself."
                    }
                ]
            }
        ],
    })
)

# Выводим статус и содержимое ответа
print("Статус:", response.status_code)
try:
    print("Ответ JSON:", response.json())
except json.JSONDecodeError:
    print("Ответ текст:", response.text)