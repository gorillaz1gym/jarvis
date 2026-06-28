class IntentEngine:

    def parse(self, text: str):
        text = text.lower()

        if text in ["exit", "выход", "стоп"]:
            return {"type": "exit"}

        # ⚡ команды
        if "открой" in text or "запусти" in text:

            if "браузер" in text or "chrome" in text:
                return {"type": "command", "action": "open_browser"}

            if "steam" in text:
                return {"type": "command", "action": "open_steam"}

            return {"type": "command", "action": "unknown"}

        return {"type": "chat"}