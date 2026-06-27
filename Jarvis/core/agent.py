class Agent:
    def __init__(self, tools=None, brain=None):
        self.tools = tools
        self.brain = brain

    def run(self, text: str):
        text = text.lower().strip()

        # =========================
        # 1. SIMPLE COMMAND ROUTING
        # =========================

        # открыть браузер
        if "браузер" in text or "chrome" in text or "гугл" in text:
            if hasattr(self.tools, "open_browser"):
                self.tools.open_browser()
                return {"text": "Открываю браузер"}

        # анализ экрана
        if "экран" in text or "что на экране" in text:
            if hasattr(self.tools, "analyze_screen"):
                result = self.tools.analyze_screen()
                return {
                    "text": "Анализирую экран",
                    "data": result
                }

        # =========================
        # 2. BRAIN (если есть)
        # =========================

        if self.brain:
            try:
                response = self.brain.think(text)

                # brain может вернуть dict или string
                if isinstance(response, dict):
                    return response

                return {"text": str(response)}

            except Exception as e:
                return {"text": "Ошибка brain", "error": str(e)}

        # =========================
        # 3. DEFAULT RESPONSE
        # =========================

        return {
            "text": "Я не понял команду"
        }