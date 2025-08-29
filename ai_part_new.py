
import requests
import json
from icecream import ic
from config import OPEN_ROUTER_API_KEY

def regeneration(markdown: str):
    ic("Starting generation")
    
    with open("prompt.txt", "r") as f:
        prompt = f.read() + (f"[{markdown}]")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "qwen/qwen3-4b:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
        })
    )
    
    if response.status_code == 200:
        try:
            result = response.json()["choices"][0]["message"]["content"]
            ic("Finishing generation", result)
            return result
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            ic("Error parsing response", str(e))
            return None
    else:
        ic("Error response", response.status_code, response.text)
        return None