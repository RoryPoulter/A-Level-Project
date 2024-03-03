from tkinter import *
import sys
import json


def loadSettings():
    with open("config.json", "r") as file:
        return json.load(file)


def loadThemes():
    with open("themes.json", "r") as file:
        return json.load(file)


def loadColourScheme():
    settings = loadSettings()
    current_theme = settings["theme"]
    colourblind_mode = settings["colourblind"]
    colourblind_schemes = {
        True: {"neg": "#FF8700", "pos": "#1E78E5"},
        False: {"neg": "#D62F2F", "pos": "#109110"}
    }
    return colourblind_schemes[colourblind_mode] | themes[current_theme]


def close():
    sys.exit()


class HintLabel(Label):
    def __init__(self, *args, **kwargs):
        """
        Label subclass which displays a ? and frame when hovered over
        """
        Label.__init__(self, *args, **kwargs)
        definition = self["text"]  # Stores the definition as a separate variable
        self["text"] = "?"  # Sets the text as "?"
        self["font"] = ("Arial", 8, "bold")  # Sets the font to bold 8pt Arial
        self.bind("<Enter>", self.on_enter)  # Binds the method on_enter when cursor enters label
        self.bind("<Leave>", self.on_leave)  # Binds the method on_leave when cursor leaves label

        self.frame = Frame(self.master, bg=colours["but_bg"])  # Creates frame for the definition

        # Label with the definition
        Label(self.frame, text=definition, bg=colours["but_bg"], fg=colours["text"], font=("Arial", 14)).pack()

    def on_enter(self, e):
        """
        Places the frame when the cursor hovers over the label
        """
        self.frame.place(x=self.winfo_x() + 50, y=self.winfo_y())  # Places the frame

    def on_leave(self, e):
        """
        Removes the frame when the cursor leaves the label
        """
        self.frame.place_forget()  # Removes the frame


class CustomButton(Button):
    def __init__(self, master, hover_background, hover_foreground, *args, **kwargs):
        """
        Button subclass which changes colours when cursor hovers over it
        :param hover_background: Background colour when cursor is above button
        :type hover_background: str
        :param hover_foreground: Foreground colour when cursor is above button
        :type hover_foreground: str
        """
        Button.__init__(self, master, *args, **kwargs)
        self["borderwidth"] = 0  # Sets the border width to 0
        self["font"] = ("Arail", 14)  # Sets the font to 14pt Arial
        self.hover_bg = hover_background
        self.hover_fg = hover_foreground
        self.bg = self["bg"]
        self.fg = self["fg"]
        self.bind("<Enter>", self.on_enter)  # Binds the method on_enter when cursor enters label
        self.bind("<Leave>", self.on_leave)  # Binds the method on_leave when cursor leaves label

    def on_enter(self, e):
        """
        Changes the colour of the button when hovered over
        """
        self.config(bg=self.hover_bg, fg=self.hover_fg)  # Changes the colour

    def on_leave(self, e):
        """
        Changes colour back to original when cursor leaves
        """
        self.config(bg=self.bg, fg=self.fg)  # Changes the colour


class MainWindow(Tk):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.geometry("600x400")
        self.title("Projectile Simulator")
        Button(self, text="Close", command=close).pack(pady=10)
        Button(self, text="Change colour", command=self.change_theme).pack()
        self.theme = "light"

        self.mainloop()

    def change_theme(self):
        theme = {"light": "dark", "dark": "light"}
        if self.theme == "dark":
            self.config(bg="#dddddd")
        else:
            self.config(bg="#333333")
        self.theme = theme.get(self.theme)


if __name__ == "__main__":
    themes = loadThemes()
    colour_scheme = loadColourScheme()
    root = MainWindow(colour_scheme)
