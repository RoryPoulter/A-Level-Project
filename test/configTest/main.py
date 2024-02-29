import json


def updateSettings(theme, colourblind):
    """
    Updates the file `config.json` with the new settings
    :param theme: The current theme
    :type theme: str
    :param colourblind: If colourblind mode is active
    :type colourblind: bool
    """
    with open("config.json", "r") as file:
        data = json.load(file)
    data |= {"theme": theme, "colourblind": colourblind}
    new_data = json.dumps(data, indent=2)
    with open("config.json", "w") as file:
        file.write(new_data)


if __name__ == "__main__":
    theme = "Light"
    colourblind = True
    updateSettings(theme, colourblind)
