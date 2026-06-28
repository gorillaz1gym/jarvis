import json
import os

class Memory:

    def __init__(self):
        self.file = "memory.json"
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file):
            return json.load(open(self.file, "r", encoding="utf-8"))
        return {"log": []}

    def save(self):
        json.dump(self.data, open(self.file, "w", encoding="utf-8"), indent=2)

    def add(self, role, text):
        self.data["log"].append({"role": role, "text": text})
        self.data["log"] = self.data["log"][-30:]
        self.save()

    def context(self):
        return [
            {"role": i["role"], "content": i["text"]}
            for i in self.data["log"]
        ]