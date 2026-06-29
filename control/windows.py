import os

def execute(action: dict):

    if not action:
        return "fail"

    name = action.get("name", "")

    apps = {
        "steam": "steam",
        "opera": "opera",
        "browser": "opera"
    }

    if name in apps:
        try:
            os.system(apps[name])
            return "ok"
        except:
            return "fail"

    return "fail"