from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Embedding the graph
import matplotlib.pyplot as plt  # Graph


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


def loadTheme():
    """
    Creates a dictionary storing the appearance options for different TKinter widgets using the chosen theme
    :return: a dictionary storing the appearance options for different TKinter widgets
    :rtype: dict[str, dict[str, str | int| tuple[str, int]]]
    """
    style = {
        "button": {
            "bg": colours["but_bg"],
            "fg": colours["text"],
            "borderwidth": 0,
            "font": ("Arial", 14),
            "hover_background": colours["accent"],
            "hover_foreground": colours["text"]
        },
        "tool button": {
            "bg": colours["bg"],
            "fg": colours["text"],
            "hover_background": colours["accent"],
            "hover_foreground": colours["text"],
            "activebackground": colours["bg"],
            "activeforeground": colours["text"],
            "width": 5,
            "height": 3
        },
        "pos button": {
            "bg": colours["pos"],
            "fg": "#FFFFFF",
            "borderwidth": 0,
            "font": ("Arial", 14)
        },
        "neg button": {
            "bg": colours["neg"],
            "fg": "#FFFFFF",
            "borderwidth": 0,
            "font": ("Arial", 14)
        },
        "label": {
            "bg": colours["bg"],
            "fg": colours["text"],
            "font": ("Arial", 14)
        },
        "label 2": {
            "bg": colours["bg"],
            "fg": colours["text"],
            "font": ("Arial", 9)
        },
        "entry": {
            "bg": colours["but_bg"],
            "fg": colours["text"],
            "font": ("Arial", 14),
            "borderwidth": 0
        },
        "checkbutton": {
            "bg": colours["bg"],
            "fg": colours["text"],
            "font": ("Arial", 14),
            "activeforeground": colours["text"],
            "activebackground": colours["bg"],
            "selectcolor": colours["accent"]
        },
        "menu": {
            "bg": colours["but_bg"],
            "fg": colours["text"],
            "highlightbackground": colours["bg"],
            "font": ("Arial", 12),
            "borderwidth": 0,
            "activebackground": colours["but_bg"],
            "activeforeground": colours["text"]
        },
        "radiobutton": {
            "bg": colours["bg"],
            "fg": colours["text"],
            "font": ("Arial", 14),
            "activeforeground": colours["text"],
            "activebackground": colours["bg"],
            "selectcolor": colours["bg"]
        }
    }

    return style


def displayGraph():
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(list(range(10)),
               list(range(10)),
               list(range(10)))


def run(): ...


def openDatabaseWindow(): ...


def close(): quit()


def openSettingsWindow():
    """
    Opens the settings window
    """
    global settings_win
    settings_win = Toplevel(root)
    settings_win.resizable(False, False)  # Keeps window the same size
    settings_win.title("Settings")
    settings_win.geometry("400x250+760+415")  # Opens the window in the middle of the screen
    settings_win.grab_set()  # Forces window above main window
    loadSettingsFrame(settings_win)


def loadSettingsFrame(win):
    """
    Loads the widgets on the settings window
    :param win: The toplevel window
    :type win: Toplevel
    """
    settings_frame = Frame(win, bg=colours["bg"])
    settings_frame.place(x=0, y=0, width=400, height=250)

    Label(settings_frame, **style["label"], text="Settings").place(relx=0.5, y=30, anchor=CENTER)
    Label(settings_frame, **style["label"], text="Theme:").place(x=50, y=70)

    theme_menu = OptionMenu(settings_frame, current_theme, *themes)
    theme_menu.config(**style["menu"], width=10)
    theme_menu.place(x=120, y=70)

    Checkbutton(settings_frame, **style["checkbutton"], text="Colourblind Mode",
                variable=colourblind_mode).place(x=50, y=120)

    Button(settings_frame, bg=colours["but_bg"], fg=colours["text"], text="Confirm", command=updateScheme,
           borderwidth=0).pack(anchor="s", side=RIGHT)


def setupInterface(window):
    """
    Creates the GUI
    :param window: the window
    :type window: Tk
    """
    def toggleDrag():
        """
        Toggles whether drag is included
        """
        global drag
        if drag.get() == "no drag":
            for entry in (m_entry, rho_entry, cd_entry, a_entry):
                entry.config(state="disabled")

        else:
            for entry in (m_entry, rho_entry, cd_entry, a_entry):
                entry.config(state="normal")

    window.title("Projectile Simulator")
    window.attributes("-fullscreen", True)
    window.config(bg=colours.get("accent"))

    # Tools
    tools_frame = Frame(bg=colours["bg"])
    tools_frame.place(x=0, y=0, width=1920, height=40)

    CustomButton(tools_frame, hover_background=colours["neg"], hover_foreground="#FFFFFF", bg=colours["bg"],
                 text="X", fg=colours["text"], height=3, width=5,
                 command=close, activebackground=colours["neg"],
                 activeforeground="#FFFFFF").pack(anchor="e", side=RIGHT)

    CustomButton(tools_frame, **style["tool button"], text="_", command=root.iconify).pack(anchor="e", side=RIGHT)
    CustomButton(tools_frame, **style["tool button"], text="💾", command=openDatabaseWindow).pack(side=LEFT)
    CustomButton(tools_frame, **style["tool button"], text="⚙", command=openSettingsWindow).pack(side=LEFT)

    # Input
    input_frame = Frame(root, bg=colours["bg"])
    input_frame.place(x=0, y=41, width=899, height=550)

    Label(input_frame, **style["label"], text="Velocity [m/s]:").place(x=20, y=20)
    Entry(input_frame, **style["entry"], width=9, textvariable=initial_velocity).place(x=200, y=20)
    Label(input_frame, **style["label"], text="Elevation Angle [°]:").place(x=20, y=60)
    Entry(input_frame, **style["entry"], width=9, textvariable=elevation_angle).place(x=200, y=60)
    Label(input_frame, **style["label"], text="Azimuth Angle [°]:").place(x=20, y=100)
    Entry(input_frame, **style["entry"], width=9, textvariable=azimuth_angle).place(x=200, y=100)
    Label(input_frame, **style["label"], text="x:").place(x=20, y=140)
    Entry(input_frame, **style["entry"], width=9, textvariable=x0).place(x=200, y=140)
    Label(input_frame, **style["label"], text="y:").place(x=20, y=180)
    Entry(input_frame, **style["entry"], width=9, textvariable=y0).place(x=200, y=180)
    Label(input_frame, **style["label"], text="z:").place(x=20, y=220)
    Entry(input_frame, **style["entry"], width=9, textvariable=z0).place(x=200, y=220)
    Label(input_frame, **style["label"], text="Gravity [m/s²]:").place(x=20, y=260)
    Entry(input_frame, **style["entry"], width=9, textvariable=gravity).place(x=200, y=260)
    Label(input_frame, **style["label"], text="Mass [kg]:").place(x=20, y=300)
    m_entry = Entry(input_frame, **style["entry"], width=9, textvariable=mass)
    m_entry.place(x=200, y=300)
    Label(input_frame, **style["label"], text="Air Density [kg/m³]:").place(x=20, y=340)
    rho_entry = Entry(input_frame, **style["entry"], width=9, textvariable=air_density)
    rho_entry.place(x=200, y=340)
    Label(input_frame, **style["label"], text="Drag Coefficient:").place(x=20, y=380)
    cd_entry = Entry(input_frame, **style["entry"], width=9, textvariable=drag_coefficient)
    cd_entry.place(x=200, y=380)
    Label(input_frame, **style["label"], text="Surface Area [m²]:").place(x=20, y=420)
    a_entry = Entry(input_frame, **style["entry"], width=9, textvariable=surface_area)
    a_entry.place(x=200, y=420)

    if drag.get() == "no drag":
        for entry in (m_entry, rho_entry, cd_entry, a_entry):
            entry.config(state="disabled")

    CustomButton(input_frame, **style["button"], text="Run", width=10, command=run).place(x=380, y=480)

    with open("definitions.txt", "r", encoding="UTF-8") as definition_file:  # Opens the file definitions.txt
        for x, line in enumerate(definition_file):  # Iterates over each line in the file
            HintLabel(input_frame, text=(line.strip()).replace(";", "\n"), bg=colours["but_bg"],
                      fg=colours["text"], width=2).place(x=330, y=40 * x + 20)

    # Checkbutton(input_frame, **style["checkbutton"], text="Compare Drag",
    #             command=toggleComparison).place(x=300, y=480)

    Radiobutton(input_frame, **style["radiobutton"], text="No Drag", variable=drag, value="no drag",
                command=toggleDrag).place(x=20, y=480)
    Radiobutton(input_frame, **style["radiobutton"], text="Drag", variable=drag, value="drag",
                command=toggleDrag).place(x=140, y=480)
    Radiobutton(input_frame, **style["radiobutton"], text="Compare", variable=drag, value="compare",
                command=toggleDrag).place(x=260, y=480)

    # Result
    output_frame = Frame(root, bg=colours["bg"])
    output_frame.place(x=0, y=592, width=899, height=488)

    Label(output_frame, **style["label"], text="Final Velocity [m/s]:", anchor="e", width=15).place(x=20, y=20)
    Label(output_frame, **style["label"], text="Displacement [m]:", anchor="e", width=15).place(x=20, y=70)
    Label(output_frame, **style["label"], text="Position:", anchor="e", width=15).place(x=20, y=120)
    Label(output_frame, **style["label"], text="Flight Duration [s]:", anchor="e", width=15).place(x=20, y=170)
    Label(output_frame, **style["label"], text="Max Height [m]:", anchor="e", width=15).place(x=20, y=220)
    Label(output_frame, **style["label"], text="Time [s]:", anchor="e", width=15).place(x=20, y=270)

    Label(output_frame, **style["label"], textvariable=velocity).place(x=200, y=20)
    Label(output_frame, **style["label"], textvariable=displacement).place(x=200, y=70)
    Label(output_frame, **style["label"], textvariable=position).place(x=200, y=120)
    Label(output_frame, **style["label"], textvariable=landing_time).place(x=200, y=170)
    Label(output_frame, **style["label"], textvariable=max_height).place(x=200, y=220)
    Label(output_frame, **style["label"], textvariable=time).place(x=200, y=270)

    # Graph frame
    graph_frame = Frame(root, bg=colours["bg"])
    graph_frame.place(x=900, y=41, width=1020, height=1039)
    display_frame = Frame(graph_frame, bg=colours["but_bg"])
    display_frame.place(x=25, y=25, width=970, height=970)
    canvas = FigureCanvasTkAgg(fig, master=display_frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)  # this is necessary on Windows to prevent


if __name__ == "__main__":
    colours = {"bg": "#2E3142", "text": "#FFFFFF", "but_bg": "#555F70", "accent": "#a379e7", "neg": "#D62F2F", "pos": "#109110"}
    style = loadTheme()
    root = Tk()

    drag = StringVar(value="no drag")
    # Inputs
    initial_velocity = StringVar()
    elevation_angle = StringVar()
    azimuth_angle = StringVar()
    x0 = StringVar()
    y0 = StringVar()
    z0 = StringVar()
    gravity = StringVar()
    mass = StringVar()
    air_density = StringVar()
    drag_coefficient = StringVar()
    surface_area = StringVar()

    # Results
    position = StringVar(value="__________, __________, __________")
    velocity = StringVar(value="__________")
    displacement = StringVar(value="__________")
    landing_time = StringVar(value="__________")
    max_height = StringVar(value="__________")
    time = StringVar(value="__________")
    fig = plt.figure()
    setupInterface(root)
    root.mainloop()
