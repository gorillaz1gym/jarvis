import base64
import requests
import os
import json

API_KEY = os.getenv("OPENROUTER_API_KEY")


def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def analyze_screen(image_path):
    print("=== SCREEN DEBUG ===")
    print("Путь:", image_path)
    print("Файл существует:", os.path.exists(image_path))

    if not os.path.exists(image_path):
        print("ФАЙЛ НЕ НАЙДЕН!")
        return {
            "screen": "unknown",
            "apps": [],
            "state": "error"
        }

    print("Размер:", os.path.getsize(image_path), "байт")
    print("===================")

    img = encode_image(image_path)

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "temperature": 0.2,
                "max_tokens": 200,
                "messages": [
                    {
                        "role": "system",
                        "content":
                            'Analyze the screenshot and return ONLY JSON: '
                            '{"screen":"...","apps":[],"state":"ok"}'
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe the screenshot briefly."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img}"
                                }
                            }
                        ]
                    }
                ]
            },
            timeout=60
        )

        print("STATUS:", res.status_code)
        print("RESPONSE:", res.text)

        data = res.json()

        if "error" in data:
            print("OPENROUTER ERROR:", data["error"]["message"])

            return {
                "screen": "unknown",
                "apps": [],
                "state": "error"
            }

        text = data["choices"][0]["message"]["content"]
        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print("VISION ERROR:", e)

        return {
            "screen": "unknown",
            "apps": [],
            "state": "error"
        }