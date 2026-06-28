import os

def run_tool(action):

    tools = {
        "open_browser": lambda: os.system("start chrome"),
        "open_steam": lambda: os.system("start steam"),
        "open_music": lambda: os.system("start spotify"),
    }

    if action in tools:
        tools[action]()
        return f"Выполнено: {action}"

    return "Неизвестная команда"