# The main body of code
# Created: 04/10/23
# Last edited: 21/02/24
from tkinter import *  # GUI
from tkinter import messagebox  # Error messages
import ctypes
import json  # Themes
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Embedding the graph
import matplotlib.pyplot as plt  # Graph
import projectile  # Projectile calculations
import database


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
        self["font"] = ("Arial", 14)  # Sets the font to 14pt Arial
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


def verifyInputs(values):
    """
    Checks if the inputs are valid
    :param values: list of all the inputs
    :type values: dict[str, str]
    :return: whether values are valid; True for yes, False for no
    :rtype: bool
    """
    # Checks for empty values
    if "" in values.values():
        messagebox.showerror("Error", "Empty fields")
        return False

    # Checks for string inputs
    try:
        values |= dict(map(lambda kv: (kv[0], float(kv[1])), values.items()))
    except ValueError:
        messagebox.showerror("Error", "Inputs must be numbers")
        return False

    # Passes the values into the function verifyRanges to check if values are within range
    valid = verifyRanges(drag.get(), **values)
    if not valid:
        return False

    return True  # If all checks are passed


def verifyRanges(drag_mode, velocity, ele_angle, azi_angle, x, y, z, gravity,
                 mass=None, air_density=None, drag_coefficient=None, area=None):
    """
    Checks if the values fall within the correct ranges
    :param drag_mode: value for if drag is included, excluded, or both
    :type drag_mode: str
    :param velocity: initial velocity
    :type velocity: int | float
    :param ele_angle: elevation angle
    :type ele_angle: int | float
    :param azi_angle: azimuth angle
    :type azi_angle: int | float
    :param x: initial x coordinate
    :type x: int | float
    :param y: initial y coordinate
    :type y: int | float
    :param z: initial z coordinate
    :type z: int | float
    :param gravity: gravitational field strength
    :type gravity: int | float
    :param mass: mass
    :type mass: int | float
    :param air_density: air density
    :type air_density: int | float
    :param drag_coefficient: drag coefficient
    :type drag_coefficient: int | float
    :param area: surface area
    :type area: int | float
    :return: True if all values are valid, False if not
    :rtype: bool
    """
    if velocity <= 0:
        messagebox.showerror("Error", "Invalid input: velocity must fall within the range: 0 < u")
        return False
    if ele_angle < 0 or ele_angle > 90:
        messagebox.showerror("Error", "Invalid input: elevation angle must fall within the range: 0 ≤ θe ≤ 90")
        return False
    if azi_angle < 0 or azi_angle >= 360:
        messagebox.showerror("Error", "Invalid input: azimuth angle must fall within the range: 0 ≤ θa < 360")
        return False
    if x < 0:
        messagebox.showerror("Error", "Invalid input: x must fall within the range: 0 ≤ x")
        return False
    if y < 0:
        messagebox.showerror("Error", "Invalid input: y must fall within the range: 0 ≤ y")
        return False
    if z < 0:
        messagebox.showerror("Error", "Invalid input: z must fall within the range: 0 ≤ z")
        return False
    if gravity <= 0:
        messagebox.showerror("Error", "Invalid input: g must fall within the range: 0 < g")
        return False

    if drag_mode != "no_drag":
        if mass <= 0:
            messagebox.showerror("Error", "Invalid input: mass must fall within the range: 0 < m")
            return False
        if air_density <= 0:
            messagebox.showerror("Error", "Invalid input: air density must fall within the range: 0 < ρ")
            return False
        if drag_coefficient <= 0 or drag_coefficient > 1:
            messagebox.showerror("Error", "Invalid input: drag coefficient must fall within the range: 0 < cd ≤ 1")
            return False
        if area <= 0:
            messagebox.showerror("Error", "Invalid input: surface area must fall within the range: 0 < A")
            return False

    return True


def close():
    sys.exit()


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
        if drag.get() == "no_drag":
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

    if drag.get() == "no_drag":
        for entry in (m_entry, rho_entry, cd_entry, a_entry):
            entry.config(state="disabled")

    CustomButton(input_frame, **style["button"], text="Run", width=10, command=run).place(x=380, y=480)

    with open("definitions.txt", "r", encoding="UTF-8") as definition_file:  # Opens the file definitions.txt
        for x, line in enumerate(definition_file):  # Iterates over each line in the file
            HintLabel(input_frame, text=(line.strip()).replace(";", "\n"), bg=colours["but_bg"],
                      fg=colours["text"], width=2).place(x=330, y=40 * x + 20)

    Radiobutton(input_frame, **style["radiobutton"], text="No Drag", variable=drag, value="no_drag",
                command=toggleDrag).place(x=20, y=480)
    Radiobutton(input_frame, **style["radiobutton"], text="Drag", variable=drag, value="drag",
                command=toggleDrag).place(x=140, y=480)
    Radiobutton(input_frame, **style["radiobutton"], text="Compare", variable=drag, value="compare",
                command=toggleDrag).place(x=260, y=480)

    # Results
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

    # Graph
    graph_frame.config(bg=colours["bg"]),
    graph_frame.place(x=900, y=41, width=1020, height=1039)


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


def updateScheme():
    """
    Updates the dictionary colours with the new theme
    """
    global style
    colours.update(themes[current_theme.get()])  # Updates the colours dictionary with the values of the chosen theme

    if colourblind_mode.get():  # If colourblind mode is on
        colours.update({"neg": "#FF8700", "pos": "#1E78E5"})
    else:  # If colourblind mode is off
        colours.update({"neg": "#D62F2F", "pos": "#109110"})

    style = loadTheme()  # Reloads the styles with the new theme
    loadFrames()  # Reloads the frames with the new theme
    updateSettings(current_theme.get(), colourblind_mode.get())


def loadFrames():
    """
    Loads all the frames and the settings window with the new colours
    """
    root.config(bg=colours["accent"])
    loadSettingsFrame(settings_win)
    setupInterface(root)


def loadTheme():
    """
    Creates a dictionary storing the appearance options for different tkinter widgets using the chosen theme
    :return: a dictionary storing the appearance options for different tkinter widgets
    :rtype: dict[str, dict[str, str | int| tuple[str, int]]]
    """
    widget_style = {
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

    return widget_style


def run():
    """
    Runs the simulation using the provided inputs
    """
    # Stores all inputs as a list
    values = {
        "velocity": initial_velocity.get(),
        "ele_angle": elevation_angle.get(),
        "azi_angle": azimuth_angle.get(),
        "x": x0.get(),
        "y": y0.get(),
        "z": z0.get(),
        "gravity": gravity.get()
    }
    if drag.get() != "no_drag":
        values |= {
            "mass": mass.get(),
            "air_density": air_density.get(),
            "drag_coefficient": drag_coefficient.get(),
            "area": surface_area.get()
        }

    valid = verifyInputs(values)  # Checks if the inputs are valid
    if not valid:
        return

    dt = 0.01
    fig = plt.figure()
    if drag.get() != "compare":
        # Creates the objects using the values
        if drag.get() == "drag":
            proj = projectile.ProjectileDrag(**values, colour=colours["pos"])
        else:
            proj = projectile.ProjectileNoDrag(**values, colour=colours["neg"])
        # Updates the position until it is on the ground
        while proj.pos[2] >= 0:
            proj.move(dt)

        if drag.get() == "drag":
            position.set(", ".join(str(round(x, 5)) for x in proj.pos))
            landing_time.set(str(round(proj.time, 5)))
        else:
            position.set(", ".join(str(round(x, 5)) for x in proj.landing_pos))
            landing_time.set(str(round(proj.landing_time, 5)))
        velocity.set(str(round(projectile.mag(proj.v), 5)))
        displacement.set(str(round(proj.calcDisplacement(), 5)))
        max_height.set(str(round(proj.max_h, 5)))
        time.set(str(round(proj.max_t, 5)))
        # loadOutputFrame()

        plot = proj.displayPath(fig)  # Creates the graph

    else:
        proj_drag = projectile.ProjectileDrag(**values, colour=colours["pos"])  # Projectile with drag
        for key in ("mass", "air_density", "drag_coefficient", "area"):
            values.pop(key)
        proj_no_drag = projectile.ProjectileNoDrag(**values, colour=colours["neg"])  # Projectile without drag

        for proj in (proj_drag, proj_no_drag):  # Iterates over each projectile
            while proj.pos[2] >= 0:  # Iterates while the projectile is above the ground
                proj.move(dt)

        plot = projectile.compare_paths(proj_drag, proj_no_drag, fig)  # Creates the graph with both projectiles
    displayGraph(fig)  # Displays the graph


def displayGraph(fig):
    """
    Displays the graph on the graph frame
    :param fig: matplotlib figure
    """
    display_frame = Frame(graph_frame, bg=colours["but_bg"])
    display_frame.place(x=25, y=25, width=970, height=970)
    canvas = FigureCanvasTkAgg(fig, master=display_frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)  # this is necessary on Windows to prevent


def openDatabaseWindow():
    """
    Opens the database window
    """
    def loadDatabaseMenuFrame():
        """
        Loads the menu frame
        """
        db_menu_frame = Frame(database_win, bg=colours["bg"])
        db_menu_frame.place(x=0, y=26, width=800, height=374)
        Label(db_menu_frame, **style["label"], text="Manage Presets").place(relx=0.5, y=50, anchor=CENTER)
        CustomButton(db_menu_frame, **style["button"], text="Save Preset", width=12,
                     command=loadDatabaseSaveFrame).place(x=250, y=250, anchor=CENTER)
        CustomButton(db_menu_frame, **style["button"], text="View Presets", width=12,
                     command=loadDatabaseViewFrame).place(x=550, y=250, anchor=CENTER)

    def loadDatabaseViewFrame():
        """
        Loads the view frame to view, load, and delete presets
        """
        def deleteRecord():
            """
            Deletes a specified record from the database
            """
            record_name = chosen_record.get()
            if record_name == "Select Preset" or record_name == "No Presets":
                return
            db.deleteRecord("Presets", "name", record_name)
            # c.execute("DELETE FROM Presets WHERE name=?", [record_name])  # Deletes the chosen preset
            # db.commit()  # Commits the changes
            records.remove(record_name)
            messagebox.showinfo("Preset Deleted", "Preset successfully deleted")

        def loadRecord():
            """
            Loads a specified record from the database to the main window
            """
            global drag
            record_name = chosen_record.get()
            if record_name == "Select Preset" or record_name == "No Presets":
                return

            record = db.selectPreset(record_name)
            drag.set(record[0])

            for value, variable in zip(record[1:8],
                                       [initial_velocity, elevation_angle, azimuth_angle, x0, y0, z0, gravity]):
                variable.set(value=value)

            if drag.get() != "no_drag":
                for value, variable in zip(record[8:], [air_density, mass, drag_coefficient, surface_area]):
                    variable.set(value=value)

            setupInterface(root)

        def previewRecord():
            """
            Loads a specified record from the database to the view frame to be previewed
            """
            record_name = chosen_record.get()
            if record_name == "Select Preset":
                return

            record = db.selectPreset(record_name)
            record_drag = record[0]
            drag_label.config(text=record_drag)
            v_label.config(text=record[1])
            ele_label.config(text=record[2])
            azi_label.config(text=record[3])
            x_label.config(text=record[4])
            y_label.config(text=record[5])
            z_label.config(text=record[6])
            g_label.config(text=record[7])

            if record_drag != "no_drag":
                m_label.config(text=record[9])
                rho_label.config(text=record[8])
                cd_label.config(text=record[10])
                a_label.config(text=record[11])
            else:
                m_label.config(text="")
                rho_label.config(text="")
                cd_label.config(text="")
                a_label.config(text="")

        db_view_frame = Frame(database_win, bg=colours["bg"])
        db_view_frame.place(x=0, y=26, width=800, height=374)
        Label(db_view_frame, bg=colours["bg"], fg=colours["text"], text="View Presets",
              font=("Calibri", 20)).place(relx=0.5, y=50, anchor=CENTER)

        # Fetches all records to be displayed in dropdown menu
        # c.execute("SELECT name, drag FROM Presets")
        # records = list(dict(c.fetchall()).keys())
        records = db.getPresets()

        preview_button = CustomButton(db_view_frame, **style["button"], text="Preview", command=previewRecord,
                                      disabledforeground=colours["text"])
        preview_button.place(x=250, y=120)
        chosen_record = StringVar(database_win)
        chosen_record.set("Select Preset")
        try:
            preset_menu = OptionMenu(db_view_frame, chosen_record, *records)
        except TypeError:  # Runs if there are no records in Presets table
            chosen_record.set("No Presets")
            records = [" "]
            preset_menu = OptionMenu(db_view_frame, chosen_record, *records)
            preset_menu.config(state="disabled", disabledforeground=colours["text"])
            preview_button.config(state="disabled")
        preset_menu.config(**style["menu"], width=10)
        preset_menu.place(x=100, y=120)

        Label(db_view_frame, **style["label 2"], text="v [m/s]:", anchor="e", width=10).place(x=120, y=170)
        Label(db_view_frame, **style["label 2"], text="θe [°]:", anchor="e", width=10).place(x=120, y=190)
        Label(db_view_frame, **style["label 2"], text="θa [°]:", anchor="e", width=10).place(x=120, y=210)
        Label(db_view_frame, **style["label 2"], text="x:", anchor="e", width=10).place(x=120, y=230)
        Label(db_view_frame, **style["label 2"], text="y:", anchor="e", width=10).place(x=120, y=250)
        Label(db_view_frame, **style["label 2"], text="z:", anchor="e", width=10).place(x=120, y=270)
        Label(db_view_frame, **style["label 2"], text="g [m/s²]:", anchor="e", width=10).place(x=120, y=290)

        v_label = Label(db_view_frame, **style["label 2"])
        ele_label = Label(db_view_frame, **style["label 2"])
        azi_label = Label(db_view_frame, **style["label 2"])
        x_label = Label(db_view_frame, **style["label 2"])
        y_label = Label(db_view_frame, **style["label 2"])
        z_label = Label(db_view_frame, **style["label 2"])
        g_label = Label(db_view_frame, **style["label 2"])

        for count, label in enumerate((v_label, ele_label, azi_label, x_label, y_label, z_label, g_label)):
            label.place(x=200, y=170 + count * 20)

        Label(db_view_frame, **style["label 2"], text="Drag:", anchor="e", width=10).place(x=350, y=170)
        Label(db_view_frame, **style["label 2"], text="m [kg]:", anchor="e", width=10).place(x=350, y=190)
        Label(db_view_frame, **style["label 2"], text="ρ [kg/m³]:", anchor="e", width=10).place(x=350, y=210)
        Label(db_view_frame, **style["label 2"], text="C:", anchor="e", width=10).place(x=350, y=230)
        Label(db_view_frame, **style["label 2"], text="A [m²]:", anchor="e", width=10).place(x=350, y=250)

        drag_label = Label(db_view_frame, **style["label 2"])
        m_label = Label(db_view_frame, **style["label 2"])
        rho_label = Label(db_view_frame, **style["label 2"])
        cd_label = Label(db_view_frame, **style["label 2"])
        a_label = Label(db_view_frame, **style["label 2"])

        for count, label in enumerate((drag_label, m_label, rho_label, cd_label, a_label)):
            label.place(x=430, y=170 + count * 20)

        CustomButton(db_view_frame, **style["button"], text="Load", width=10, command=loadRecord).place(x=600, y=220)
        Button(db_view_frame, **style["neg button"], text="Delete", width=10, command=deleteRecord).place(x=600, y=270)

    def loadDatabaseSaveFrame():
        """
        Loads the save frame to save new presets
        """
        def saveRecord():
            """
            Saves a new preset to the database using values from the main window
            """
            name = new_preset.get()
            records = db.selectRecord("name", "Presets", {"name": name})  # Selects all records with the same name
            if records:  # If the name is not unique
                messagebox.showerror("Error", "Invalid input: name already in use")
                return
            if len(name) > 20:  # If the name is too long
                messagebox.showerror("Error", "Invalid input: name must be at most 20 characters")
                return
            elif name == "":  # If the field is empty
                messagebox.showerror("Error", "Invalid input: name field empty")
                return
            motion_record = {
                "velocity": initial_velocity.get(),
                "ele_angle": elevation_angle.get(),
                "azi_angle": azimuth_angle.get(),
                "x": x0.get(),
                "y": y0.get(),
                "z": z0.get(),
            }
            environment_record = {
                "gravity": gravity.get()
            }
            if drag.get() != "no_drag":
                environment_record |= {
                    "air_density": air_density.get()
                }
                projectile_record = {
                    "mass": mass.get(),
                    "drag_coefficient": drag_coefficient.get(),
                    "area": surface_area.get()
                }
            else:
                environment_record |= {
                    "air_density": -1
                }
                projectile_record = {
                    "mass": -1,
                    "drag_coefficient": -1,
                    "area": -1
                }
            values = motion_record | environment_record | projectile_record

            valid = verifyInputs(values)  # Checks if the inputs are valid
            if not valid:
                return
            if drag.get() == "no_drag":
                environment_record["air_density"] = None
                projectile_record["mass"] = None
                projectile_record["drag_coefficient"] = None
                projectile_record["area"] = None

            # Finds environment id
            eid = db.duplicateCheck("EID", "Environments", environment_record)

            # Finds projectile id
            pid = db.duplicateCheck("PID", "Projectiles", projectile_record)

            # Finds motion id
            mid = db.duplicateCheck("MID", "Motion", motion_record)

            # Checks if the preset is unique
            repeats = db.selectRecord("name", "Presets", {"drag": drag.get(), "EID": eid, "PID": pid, "MID": mid})
            if not repeats:  # If the preset is unique
                db.insertRecord("Presets", {"name": name, "drag": drag.get(), "EID": eid, "PID": pid, "MID": mid})
                messagebox.showinfo("Preset Saved", "Preset successfully saved")
            else:  # If it already exists
                messagebox.showerror("Error", f"Invalid value/s: record already exists under '{repeats[0][0]}'")
                return

        new_preset = StringVar(database_win)  # The name of the new preset
        db_save_frame = Frame(database_win, bg=colours["bg"])
        db_save_frame.place(x=0, y=26, width=800, height=374)
        Label(db_save_frame, **style["label"], text="Save Preset").place(relx=0.5, y=50, anchor=CENTER)
        Label(db_save_frame, **style["label"], text="Name:").place(relx=0.5, y=150, anchor=CENTER)
        Entry(db_save_frame, **style["entry"], textvariable=new_preset).place(relx=0.5, y=175, anchor=CENTER)
        Button(db_save_frame, **style["pos button"], text="Save Preset",
               command=saveRecord).place(relx=0.5, y=225, anchor=CENTER)

    database_win = Toplevel(root)
    database_win.resizable(False, False)
    database_win.title("Database")
    database_win.geometry("800x400+560+340")
    database_win.grab_set()
    db_tool_frame = Frame(database_win, bg=colours["bg"])
    db_tool_frame.place(x=0, y=0, width=800, height=26)
    Button(db_tool_frame, text="X", bg=colours["neg"], fg="#FFFFFF", borderwidth=0,
           font=("Calibri", 16), command=loadDatabaseMenuFrame).pack(anchor="e")
    loadDatabaseMenuFrame()


if __name__ == "__main__":
    db = database.Database("presets.db")

    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()

    with open("config.json", "r") as settings_file:  # Opens file config.json
        settings = json.load(settings_file)  # Loads the data
    last_theme = settings["theme"]  # Last used theme
    last_colourblind = settings["colourblind"]  # Last used colourblind setting

    colourblind_schemes = {
        True: {"neg": "#FF8700", "pos": "#1E78E5"},
        False: {"neg": "#D62F2F", "pos": "#109110"}
    }

    with open("themes.json", "r") as themes_file:  # Opens file themes.json
        themes = json.load(themes_file)  # Loads all themes to dictionary
    colours = colourblind_schemes[last_colourblind]  # Stores the current theme
    colours.update(themes[last_theme])
    current_theme = StringVar(value=last_theme)  # Variable to store the current theme
    colourblind_mode = BooleanVar(value=last_colourblind)  # Boolean value for if colourblind mode is active
    style = loadTheme()  # Stores the style options for different widgets

    graph_frame = Frame(root)

    # Inputs
    drag = StringVar(value="no_drag")  # Options: "no_drag", "drag", "compare"
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

    setupInterface(root)  # Loads the GUI

    root.mainloop()  # Keeps the window open
