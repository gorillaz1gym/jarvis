class IntentEngine:

    def parse(self, text: str):
        t = text.lower()

        # exit
        if t in ["exit", "выход", "стоп"]:
            return {"type": "exit"}

        # multiple actions
        actions = []

        if "браузер" in t:
            actions.append("open_browser")

        if "steam" in t:
            actions.append("open_steam")

        if "музыку" in t:
            actions.append("open_music")

        if actions:
            return {
                "type": "multi_command",
                "actions": actions
            }

        return {"type": "chat"}