class Agent:

    def __init__(self, tools=None, brain=None):
        self.tools = tools
        self.brain = brain

    def run(self, text: str):

        plan = self.brain.think(text)

        action = plan.get("action")
        inp = plan.get("input", "")

        try:

            # =====================
            # OPEN APP
            # =====================
            if action == "open_app":
                ok = self.tools.open_app(inp)

                if ok:
                    return {"text": f"Открываю {inp}"}
                else:
                    return {"text": f"Не удалось найти {inp}"}

            # =====================
            # TYPE TEXT
            # =====================
            if action == "type":
                self.tools.type_text(inp)
                return {"text": "Печатаю текст"}

            # =====================
            # PRESS KEY
            # =====================
            if action == "press":
                self.tools.press_key(inp)
                return {"text": f"Нажимаю {inp}"}

            # =====================
            # SCREEN ANALYSIS
            # =====================
            if action == "analyze_screen":
                data = self.tools.analyze_screen()
                return {
                    "text": "Смотрю экран",
                    "data": data
                }

            # =====================
            # CHAT FALLBACK
            # =====================
            return {"text": inp}

        except Exception as e:
            return {"text": f"Ошибка Agent: {e}"}