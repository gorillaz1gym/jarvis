from core.tools import run_tool

class Router:

    def route(self, intent, text, brain, memory, tools):

        # 🚪 EXIT
        if intent["type"] == "exit":
            return {
                "type": "exit",
                "text": "Выключаюсь"
            }

        # ⚡ COMMAND MODE
        if intent["type"] == "command":

            if intent["action"] == "open_browser":
                return {
                    "type": "command",
                    "action": lambda: tools.open_browser(),
                    "text": None
                }

            return {
                "type": "command",
                "action": None,
                "text": "Неизвестная команда"
            }

        # 👁 VISION MODE
        if intent["type"] == "vision":
            return {
                "type": "vision",
                "text": tools.analyze_screen()
            }

        # 🧠 CHAT MODE (DEFAULT)
        messages = memory.context()
        messages.append({"role": "user", "content": text})

        response = brain.ask(messages)

        return {
            "type": "chat",
            "text": response["text"]
        }