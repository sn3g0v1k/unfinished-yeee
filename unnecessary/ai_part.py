from g4f.client import Client
from icecream import ic

def regeneration(markdown: str):
    ic("Starting generation")
    with open("prompt.txt", "r") as f:
        prompt = f.read()+(f"[{markdown}]")


    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        web_search=False
    )
    ic("Finishing generation", response.choices[0].message.content)
    return response.choices[0].message.content