# The main body of code
# Created: 04/10/23
# Last edited: 29/01/24
from tkinter import *  # GUI
from tkinter import messagebox  # Error messages
import json  # Themes
import projectile  # Projectile calculations
import sqlite3  # Database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Embedding the graph
import matplotlib.pyplot as plt  # Graph
import ctypes


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


def verifyInputs(values):
    """
    Checks if the inputs are valid
    :param values: list of all the inputs
    :type values: list[int | float | bool | None]
    :return: whether values are valid; True for yes, False for no
    :rtype: bool
    """
    # Checks for empty values
    if "" in values:
        messagebox.showerror("Error", "Empty fields")
        return False

    # Checks for string inputs
    try:
        values[0:7] = list(map(float, values[0:7]))
        if drag:
            values[8:] = list(map(float, values[8:]))
    except ValueError:
        messagebox.showerror("Error", "Inputs must be numbers")
        return False

    # Passes the values into the function verifyRanges to check if values are within range
    valid = verifyRanges(*values)
    if not valid:
        return False

    return True  # If all checks are passed


def verifyRanges(u, ele_angle, azi_angle, x, y, z, g, drag=False, m=None, rho=None, cd=None, area=None):
    """
    Checks if the values fall within the correct ranges
    :param u: initial velocity
    :type u: int | float
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
    :param g: gravitational field strength
    :type g: int | float
    :param drag: boolean value for if drag is included
    :type drag: bool
    :param m: mass
    :type m: int | float
    :param rho: air density
    :type rho: int | float
    :param cd: drag coefficient
    :type cd: int | float
    :param area: surface area
    :type area: int | float
    :return: True if all values are valid, False if not
    :rtype: bool
    """
    if u <= 0:
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
    if g <= 0:
        messagebox.showerror("Error", "Invalid input: g must fall within the range: 0 < g")
        return False

    if drag:
        if m <= 0:
            messagebox.showerror("Error", "Invalid input: mass must fall within the range: 0 < m")
            return False
        if rho <= 0:
            messagebox.showerror("Error", "Invalid input: air density must fall within the range: 0 < ρ")
            return False
        if cd <= 0 or cd > 1:
            messagebox.showerror("Error", "Invalid input: drag coefficient must fall within the range: 0 < cd ≤ 1")
            return False
        if area <= 0:
            messagebox.showerror("Error", "Invalid input: surface area must fall within the range: 0 < A")
            return False

    return True


def loadToolsFrame():
    """
    Loads the toolbar
    """
    tools_frame = Frame(bg=colours["bg"])
    tools_frame.place(x=0, y=0, width=1920, height=40)

    CustomButton(tools_frame, hover_background=colours["neg"], hover_foreground="#FFFFFF", bg=colours["bg"],
                 text="X", fg=colours["text"], height=3, width=5,
                 command=quit, activebackground=colours["neg"],
                 activeforeground="#FFFFFF").pack(anchor="e", side=RIGHT)

    CustomButton(tools_frame, **style["tool button"], text="_", command=root.iconify).pack(anchor="e", side=RIGHT)
    CustomButton(tools_frame, **style["tool button"], text="💾", command=openDatabaseWindow).pack(side=LEFT)
    CustomButton(tools_frame, **style["tool button"], text="⚙", command=openSettingsWindow).pack(side=LEFT)


def loadInputFrame():
    """
    Loads the input frame
    """
    def toggleComparison():
        """
        Toggles whether drag is compared
        """
        if not drag:
            toggleDrag()
        if compare_drag.get():
            drag_button.config(state="disabled")
        else:
            drag_button.config(state="normal")

    def toggleDrag():
        """
        Toggles whether drag is included
        """
        global drag
        if not drag:
            drag_button.config(text="Drag", bg=colours["pos"])
            for entry in (m_entry, rho_entry, cd_entry, a_entry):
                entry.config(state="normal")

        else:
            drag_button.config(text="No Drag", bg=colours["neg"])
            for entry in (m_entry, rho_entry, cd_entry, a_entry):
                entry.config(state="disabled")

        drag = not drag

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

    drag_button = Button(input_frame, **style["pos button"], text="Drag", width=10, command=toggleDrag)
    drag_button.place(x=20, y=480)

    if not drag:
        drag_button.config(bg=colours["neg"], text="No Drag")
        for entry in (m_entry, rho_entry, cd_entry, a_entry):
            entry.config(state="disabled")

    CustomButton(input_frame, **style["button"], text="Run", width=10, command=run).place(x=160, y=480)

    with open("definitions.txt", "r", encoding="UTF-8") as definition_file:  # Opens the file definitions.txt
        for x, line in enumerate(definition_file):  # Iterates over each line in the file
            HintLabel(input_frame, text=(line.strip()).replace(";", "\n"), bg=colours["but_bg"],
                      fg=colours["text"], width=2).place(x=330, y=40 * x + 20)

    Checkbutton(input_frame, **style["checkbutton"], text="Compare Drag", variable=compare_drag,
                command=toggleComparison).place(x=300, y=480)


def loadOutputFrame():
    """
    Loads the output frame
    """
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


def loadGraphFrame():
    """
    Loads the graph frame
    """
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


def loadFrames():
    """
    Loads all the frames and the settings window with the new colours
    """
    root.config(bg=colours["accent"])
    loadToolsFrame()
    loadSettingsFrame(settings_win)
    loadInputFrame()
    loadOutputFrame()
    loadGraphFrame()


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
        }
    }

    return style


def run():
    """
    Runs the simulation using the provided inputs
    """
    # Stores all inputs as a list
    values = [
        initial_velocity.get(),
        elevation_angle.get(),
        azimuth_angle.get(),
        x0.get(),
        y0.get(),
        z0.get(),
        gravity.get(),
        drag
    ]
    if drag:
        values += [
            mass.get(),
            air_density.get(),
            drag_coefficient.get(),
            surface_area.get()
        ]

    valid = verifyInputs(values)  # Checks if the inputs are valid
    if not valid:
        return
    values.pop(7)  # Removes the value for drag

    dt = 0.01
    fig = plt.figure()
    if not compare_drag.get():
        # Creates the objects using the values
        if drag:
            proj = projectile.ProjectileDrag(*values, colour=colours["pos"])
        else:
            proj = projectile.ProjectileNoDrag(*values, colour=colours["neg"])
        # Updates the position until it is on the ground
        while proj.pos[2] >= 0:
            proj.move(dt)

        if drag:
            position.set(", ".join(str(round(x, 5)) for x in proj.pos))
            landing_time.set(str(round(proj.time, 5)))
        else:
            position.set(", ".join(str(round(x, 5)) for x in proj.landing_pos))
            landing_time.set(str(round(proj.landing_time, 5)))
        velocity.set(str(round(projectile.mag(proj.v), 5)))
        displacement.set(str(round(proj.calcDisplacement(), 5)))
        max_height.set(str(round(proj.max_h, 5)))
        time.set(str(round(proj.max_t, 5)))
        loadOutputFrame()

        plot = proj.displayPath(fig)  # Creates the graph

    else:
        proj_drag = projectile.ProjectileDrag(*values, colour=colours["pos"])  # Projectile with drag
        proj_no_drag = projectile.ProjectileNoDrag(*values[:7], colour=colours["neg"])  # Projectile without drag

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
            c.execute("DELETE FROM Presets WHERE name=?", [record_name])  # Deletes the chosen preset
            db.commit()  # Commits the changes
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

            record = selectPreset(record_name)
            drag = bool(record[0])

            for value, variable in zip(record[1:8],
                                       [initial_velocity, elevation_angle, azimuth_angle, x0, y0, z0, gravity]):
                variable.set(value=value)

            if drag:
                for value, variable in zip(record[8:], [air_density, mass, drag_coefficient, surface_area]):
                    variable.set(value=value)

            loadInputFrame()

        def previewRecord():
            """
            Loads a specified record from the database to the view frame to be previewed
            """
            record_name = chosen_record.get()
            if record_name == "Select Preset":
                return

            record = selectPreset(record_name)
            record_drag = bool(record[0])
            v_label.config(text=record[1])
            ele_label.config(text=record[2])
            azi_label.config(text=record[3])
            x_label.config(text=record[4])
            y_label.config(text=record[5])
            z_label.config(text=record[6])
            g_label.config(text=record[7])

            if record_drag:
                drag_label.config(text="True")
                m_label.config(text=record[9])
                rho_label.config(text=record[8])
                cd_label.config(text=record[10])
                a_label.config(text=record[11])
            else:
                drag_label.config(text="False")
                m_label.config(text="")
                rho_label.config(text="")
                cd_label.config(text="")
                a_label.config(text="")

        db_view_frame = Frame(database_win, bg=colours["bg"])
        db_view_frame.place(x=0, y=26, width=800, height=374)
        Label(db_view_frame, bg=colours["bg"], fg=colours["text"], text="View Presets",
              font=("Calibri", 20)).place(relx=0.5, y=50, anchor=CENTER)

        # Fetches all records to be displayed in dropdown menu
        c.execute("SELECT name, drag FROM Presets")
        records = list(dict(c.fetchall()).keys())

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
            records = selectRecord("name", "Presets", "name", [name])  # Selects all records with the same name
            if records:  # If the name is not unique
                messagebox.showerror("Error", "Invalid input: name already in use")
                return
            if len(name) > 20:  # If the name is too long
                messagebox.showerror("Error", "Invalid input: name must be at most 20 characters")
                return
            elif name == "":  # If the field is empty
                messagebox.showerror("Error", "Invalid input: name field empty")
                return
            values = [
                initial_velocity.get(),
                elevation_angle.get(),
                azimuth_angle.get(),
                x0.get(),
                y0.get(),
                z0.get(),
                gravity.get(),
                drag
            ]
            if drag:
                values += [
                    air_density.get(),
                    mass.get(),
                    drag_coefficient.get(),
                    surface_area.get()
                ]
            else:
                values += [None] * 4  # Used as NULL values in database

            valid = verifyInputs(values)  # Checks if the inputs are valid
            if not valid:
                return

            motion_record = values[0:6]
            environment_record = values[6:9:2]
            projectile_record = values[9:]

            # Finds environment id
            eid = duplicateCheck("EID", "Environments", "gravity,air_density", environment_record)

            # Finds projectile id
            pid = duplicateCheck("PID", "Projectiles", "mass,drag_coefficient,area", projectile_record)

            # Finds motion id
            mid = duplicateCheck("MID", "Motion", "velocity,ele_angle,azi_angle,x,y,z", motion_record)

            # Checks if the preset is unique
            repeats = selectRecord("name", "Presets", "EID,PID,MID", [eid, pid, mid])
            if not repeats:  # If the preset is unique
                insertRecord("Presets", "name,drag,EID,PID,MID", [name, drag, eid, pid, mid])
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


# Database functions
def insertRecord(table, fields, values):
    """
    Runs an SQL query to insert values into a given table
    :param table: The table which the record will be inserted into
    :type table: str
    :param fields: The names of the fields in the table
    :type fields: str
    :param values: The values which will be inserted into the record
    :type values: list
    """
    q_marks = "?," * len(fields.split(","))  # Creates a string e.g. "?,?,?" with as many ?s as fields
    values = tuple(values)  # Casts list as tuple
    c.execute(f"INSERT INTO {table} ({fields}) VALUES ({q_marks[:~0]})", values)  # Inserts the record to the database
    db.commit()  # Commits the changes


def selectRecord(field, table, fields, values):
    """
    Runs an SQL select query and returns the records
    :param field: The field which the selected values belong to
    :type field: str
    :param table: The table which the record will be inserted into
    :type table: str
    :param fields: The names of the fields in the table
    :type fields: str
    :param values: The values which will be inserted into the record
    :type values: list
    :return: The records which match the chosen values
    :rtype: list
    """
    q_marks = "?," * len(fields.split(","))  # Creates a string e.g. "?,?,?" with as many ?s as fields
    c.execute(f"SELECT {field} FROM {table} WHERE ({fields}) IS ({q_marks[:~0]})", values)  # Selects the record
    return c.fetchall()


def duplicateCheck(field, table, fields, values):
    """
    Checks if the record exists; if not the record is inserted; returns the primary key
    :param field: The field which the selected values belong to
    :type field: str
    :param table: The table which the record will be inserted into
    :type table: str
    :param fields: The names of the fields in the table
    :type fields: str
    :param values: The values which will be inserted into the record
    :type values: list
    :return: the id
    :rtype: int
    """
    primary_key = selectRecord(field, table, fields, values)  # Selects the primary key from the record
    if not primary_key:  # If the record does not exist
        insertRecord(table, fields, values)  # Inserts the record
        primary_key = selectRecord(field, table, fields, values)[0][0]  # Fetches the primary key of the new record
    else:  # If the record exists
        primary_key = primary_key[0][0]  # Isolates the primary key from the record
    return primary_key


def selectPreset(name):
    """
    Selects the preset from the database
    :param name: The name (primary key) of the preset
    :type name: str
    :return: The values from the preset
    :rtype: tuple
    """
    # Selects all the values from the preset
    c.execute("""SELECT Presets.drag, 
    Motion.velocity, Motion.ele_angle, Motion.azi_angle, Motion.x, Motion.y, Motion.z, 
    Environments.gravity, Environments.air_density,
    Projectiles.mass, Projectiles.drag_coefficient, Projectiles.area
    FROM Motion, Environments, Presets, Projectiles 
    WHERE Presets.EID=Environments.EID AND Presets.PID=Projectiles.PID AND Presets.MID=Motion.MID AND 
    Presets.name=?""",
              [name])
    return c.fetchall()[0]


# Database
db = sqlite3.connect("presets.db")  # Connects to file presets.db
db.execute("PRAGMA foreign_keys = ON")  # Enables foreign keys
c = db.cursor()

# Creates the tables if they don't exist
c.execute("""CREATE TABLE IF NOT EXISTS Environments
(EID                INTEGER     PRIMARY KEY,
gravity             REAL        NOT NULL,
air_density         REAL)""")

c.execute("""CREATE TABLE IF NOT EXISTS Projectiles
(PID                INTEGER     PRIMARY KEY,
mass                REAL,
drag_coefficient    REAL,
area                REAL)""")

c.execute("""CREATE TABLE IF NOT EXISTS Motion
(MID                INTEGER     PRIMARY KEY,
velocity            REAL        NOT NULL,
ele_angle           REAL        NOT NULL,
azi_angle           REAL        NOT NULL,
x                   REAL        NOT NULL,
y                   REAL        NOT NULL,
z                   REAL        NOT NULL)""")

c.execute("""CREATE TABLE IF NOT EXISTS Presets
(name               TEXT        PRIMARY KEY,
drag                INTEGER     NOT NULL,
EID                 INTEGER     NOT NULL,
PID                 INTEGER     NOT NULL,
MID                 INTEGER     NOT NULL,
FOREIGN KEY (EID) REFERENCES Environments (EID),
FOREIGN KEY (PID) REFERENCES Projectiles (PID),
FOREIGN KEY (MID) REFERENCES Motion (MID))""")
db.commit()  # Saves any changes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.title("Projectile Simulator")
root.attributes("-fullscreen", True)


with open("themes.json", "r") as themes_file:  # Opens the JSON file
    themes = json.load(themes_file)  # Loads all themes to dictionary
colours = {"neg": "#D62F2F", "pos": "#109110"}  # Stores the current theme
colours.update(themes["Dark"])  # Sets the current theme to dark
current_theme = StringVar(value="Dark")  # Variable to store the current theme
colourblind_mode = BooleanVar(value=False)  # Boolean value for if colourblind mode is active
style = loadTheme()  # Stores the style options for different widgets

root.config(bg=colours["accent"])

graph_frame = Frame(root)

drag = False
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
compare_drag = BooleanVar(value=False)  # Boolean value whether both graphs are shown

# Results
position = StringVar(value="__________, __________, __________")
velocity = StringVar(value="__________")
displacement = StringVar(value="__________")
landing_time = StringVar(value="__________")
max_height = StringVar(value="__________")
time = StringVar(value="__________")

loadToolsFrame()  # Loads the tool frame
loadInputFrame()  # Loads the input frame
loadOutputFrame()  # Loads the results frame
loadGraphFrame()  # Loads the graph frame

root.mainloop()  # Keeps the window open
