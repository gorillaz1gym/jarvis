import json
import os

class Memory:

    def __init__(self):
        self.file = "memory.json"

        if not os.path.exists(self.file):
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save(self, user, response):

        data = self.load()

        data.append({
            "user": user,
            "response": response
        })

        data = data[-20:]  # keep last 20

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def get_context(self):

        data = self.load()

        context = ""

        for item in data[-5:]:
            context += f"USER: {item['user']}\n"

        return context