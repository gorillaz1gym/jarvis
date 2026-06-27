import os

def open_app(app):
    apps = {
        "chrome": "start chrome",
        "steam": "start steam",
        "notepad": "notepad"
    }

    if app in apps:
        os.system(apps[app])
        return f"Opened {app}"

    return "Unknown app"