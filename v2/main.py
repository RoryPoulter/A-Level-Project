from tkinter import *
from tkinter import messagebox
import json
import projectile
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import ctypes


class HintLabel(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        definition = self["text"]
        self["text"] = "?"
        self["font"] = ("Arial", 8, "bold")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.frame = Frame(self.master, bg=colours["but_bg"])

        Label(self.frame, text=definition, bg=colours["but_bg"], fg=colours["text"], font=("Arial", 14)).pack()

    def on_enter(self, e):
        self.frame.place(x=self.winfo_x() + 50, y=self.winfo_y())

    def on_leave(self, e):
        self.frame.place_forget()


class CustomButton(Button):
    def __init__(self, master, hover_background, hover_foreground, *args, **kwargs):
        Button.__init__(self, master, *args, **kwargs)
        self["borderwidth"] = 0
        self["font"] = ("Arail", 14)
        self.hover_bg = hover_background
        self.hover_fg = hover_foreground
        self.bg = self["bg"]
        self.fg = self["fg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg=self.hover_bg, fg=self.hover_fg)

    def on_leave(self, e):
        self.config(bg=self.bg, fg=self.fg)


def verifyInputs(u: float, ele_angle: float, azi_angle: float, x: float, y: float, z: float, g: float, drag=False,
                 m: float = None, rho: float = None, cd: float = None, area: float = None) -> bool:
    if u <= 0:
        messagebox.showerror("Error", "Invalid input: velocity must fall within the range: 0 < u")
        return False
    if ele_angle < 0 or ele_angle > 90:
        messagebox.showerror("Error", "Invalid input: elevation angle must fall within the range: 0 ≤ θe < 90")
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
    tools_frame = Frame(bg=colours["bg"])
    tools_frame.place(x=0, y=0, width=1920, height=40)

    CustomButton(tools_frame, hover_background=colours["neg"], hover_foreground="#FFFFFF", bg=colours["bg"],
                 text="X", fg=colours["text"], height=3, width=5,
                 command=root.quit, activebackground=colours["neg"],
                 activeforeground="#FFFFFF").pack(anchor="e", side=RIGHT)

    CustomButton(tools_frame, **style["tool button"], text="_", command=root.iconify).pack(anchor="e", side=RIGHT)
    CustomButton(tools_frame, **style["tool button"], text="💾", command=openDatabaseWindow).pack(side=LEFT)
    CustomButton(tools_frame, **style["tool button"], text="⚙", command=openSettingsWindow).pack(side=LEFT)


def loadInputFrame():
    def enable_compare():
        if not drag:
            toggle()
        if compare_drag.get():
            drag_button.config(state="disabled")
        else:
            drag_button.config(state="normal")

    def toggle():
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

    input_frame.config(bg=colours["bg"])
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

    drag_button = Button(input_frame, **style["pos button"], text="Drag", width=10, command=toggle)
    drag_button.place(x=20, y=480)

    if not drag:
        drag_button.config(bg=colours["neg"], text="No Drag")
        for entry in (m_entry, rho_entry, cd_entry, a_entry):
            entry.config(state="disabled")

    CustomButton(input_frame, **style["button"], text="Run", width=10, command=run).place(x=160, y=480)

    with open("definitions.txt", "r", encoding="UTF-8") as file:
        for x, line in enumerate(file):
            HintLabel(input_frame, text=(line.strip()).replace(";", "\n"), bg=colours["but_bg"],
                      fg=colours["text"], width=2).place(x=330, y=40 * x + 20)

    Checkbutton(input_frame, **style["checkbutton"], text="Compare Drag", variable=compare_drag,
                command=enable_compare).place(x=300, y=480)


def loadOutputFrame():
    output_frame.config(bg=colours["bg"])
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
    # global display_frame
    graph_frame.config(bg=colours["bg"]),
    graph_frame.place(x=900, y=41, width=1020, height=1039)


def openSettingsWindow():
    global settings_win
    settings_win = Toplevel(root)
    settings_win.resizable(False, False)  # Keeps window the same size
    settings_win.title("Settings")
    settings_win.geometry("400x250+760+415")
    settings_win.grab_set()  # Forces window above main window
    loadSettingsFrame(settings_win)


def loadSettingsFrame(win: Toplevel):
    settings_frame = Frame(win, bg=colours["bg"])
    settings_frame.place(x=0, y=0, width=400, height=250)

    Label(settings_frame, **style["label"], text="Settings").place(relx=0.5, y=30, anchor=CENTER)
    Label(settings_frame, **style["label"], text="Theme:").place(x=50, y=70)

    menu = OptionMenu(settings_frame, current_theme, *themes)
    menu.config(bg=colours["but_bg"], fg=colours["text"], borderwidth=0, highlightbackground=colours["bg"],
                font=("Calibri", 12), width=10, activeforeground=colours["text"], activebackground=colours["but_bg"])
    menu.place(x=120, y=70)

    Checkbutton(settings_frame, **style["checkbutton"], text="Colourblind Mode", variable=colourblind_mode).place(x=50, y=120)

    Button(settings_frame, bg=colours["but_bg"], fg=colours["text"], text="Confirm", command=updateScheme,
           borderwidth=0).pack(anchor="s", side=RIGHT)


def updateScheme():
    global style
    colours.update(themes[current_theme.get()])  # Updates the colours dictionary with the values of the chosen theme

    if colourblind_mode.get():
        colours.update({"neg": "#FF8700", "pos": "#1E78E5"})
    else:
        colours.update({"neg": "#D62F2F", "pos": "#109110"})

    style = loadTheme()
    loadFrames()  # Reloads the frames with the new theme


def loadFrames():
    root.config(bg=colours["but_bg"])
    loadToolsFrame()
    loadSettingsFrame(settings_win)
    loadInputFrame()
    loadOutputFrame()
    loadGraphFrame()


def loadTheme():
    style = {
        "button": {
            "bg": colours["but_bg"],
            "fg": colours["text"],
            "borderwidth": 0,
            "font": ("Arial", 14),
            "hover_background": colours["bg"],
            "hover_foreground": colours["text"]
        },
        "tool button": {
            "bg": colours["bg"],
            "fg": colours["text"],
            "hover_background": colours["but_bg"],
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
            "selectcolor": colours["but_bg"]
        }
    }

    return style


def run():
    # Stores all inputs as a list
    values = [
        initial_velocity.get(),
        elevation_angle.get(),
        azimuth_angle.get(),
        x0.get(),
        y0.get(),
        z0.get(),
        gravity.get()
    ]
    if drag:
        values += [
            mass.get(),
            air_density.get(),
            drag_coefficient.get(),
            surface_area.get()
        ]

    # Checks for any empty fields
    if "" in values:
        messagebox.showerror("Error", "Empty fields")
        return
    # Checks for invalid inputs
    try:
        values = list(map(float, values))
    except ValueError:
        messagebox.showerror("Error", "Inputs must be numbers")
        return

    # Passes the values into the function verifyInputs to check validity
    if drag:
        valid = verifyInputs(*values[0:6], drag, *values[6:])
    else:
        valid = verifyInputs(*values)

    if not valid:
        return

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

        ax = proj.displayPath(fig)  # Creates the graph

    else:
        proj_1 = projectile.ProjectileDrag(*values, colour=colours["pos"])  # Projectile with drag
        proj_2 = projectile.ProjectileNoDrag(*values[:7], colour=colours["neg"])  # Projectile without drag

        for proj in (proj_1, proj_2):  # Iterates over each projectile
            while proj.pos[2] >= 0:  # Iterates while the projectile os above the ground
                proj.move(dt)

        ax = projectile.compare_paths(proj_1, proj_2, fig)  # Creates the graph with both projectiles
    displayGraph(fig)  # Displays the graph


def displayGraph(fig):
    display_frame = Frame(graph_frame, bg=colours["but_bg"])
    display_frame.place(x=25, y=25, width=970, height=970)
    canvas = FigureCanvasTkAgg(fig, master=display_frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)  # this is necessary on Windows to prevent


def openDatabaseWindow():

    def loadDatabaseMenuFrame():
        db_menu_frame = Frame(database_win, bg=colours["bg"])
        db_menu_frame.place(x=0, y=26, width=800, height=374)
        Label(db_menu_frame, **style["label"], text="Manage Presets").place(relx=0.5, y=50, anchor=CENTER)
        CustomButton(db_menu_frame, **style["button"], text="Save Preset", width=12,
                     command=loadDatabaseSaveFrame).place(x=250, y=250, anchor=CENTER)
        CustomButton(db_menu_frame, **style["button"], text="View Presets", width=12,
                     command=loadDatabaseViewFrame).place(x=550, y=250, anchor=CENTER)

    def loadDatabaseViewFrame():
        def deleteRecord():
            record_name = chosen_record.get()
            if record_name == "Select Preset" or record_name == "No Presets":
                return
            c.execute("DELETE FROM Presets WHERE name=?", [record_name])
            db.commit()
            records.remove(record_name)
            messagebox.showinfo("Preset Deleted", "Preset successfully deleted")

        def loadRecord():
            global drag
            record_name = chosen_record.get()
            if record_name == "Select Preset" or record_name == "No Presets":
                return
            c.execute("""SELECT Motion.velocity, Motion.ele_angle, Motion.azi_angle, Motion.x, Motion.y, Motion.z, 
                        Environments.gravity, Presets.drag, 
                        Environments.air_density,
                        Projectiles.mass, Projectiles.drag_coefficient, Projectiles.area
                        FROM Motion, Environments, Presets, Projectiles 
                        WHERE Presets.EID=Environments.EID AND Presets.PID=Projectiles.PID AND Presets.MID=Motion.MID AND 
                        Presets.name=?""",
                      [record_name])
            record = c.fetchall()[0]
            drag = bool(record[8])

            for value, variable in zip(record[:7], [initial_velocity, elevation_angle, azimuth_angle, x0, y0, z0, gravity]):
                variable.set(value=value)

            if drag:
                for value, variable in zip(record[8:], [air_density, mass, drag_coefficient, surface_area]):
                    variable.set(value=value)

            loadInputFrame()

        def previewRecord():
            record_name = chosen_record.get()
            if record_name == "Select Preset":
                return
            c.execute("""SELECT Motion.velocity, Motion.ele_angle, Motion.azi_angle, Motion.x, Motion.y, Motion.z, 
            Environments.gravity, Environments.air_density,
            Presets.drag, 
            Projectiles.mass, Projectiles.drag_coefficient, Projectiles.area
            FROM Motion, Environments, Presets, Projectiles 
            WHERE Presets.EID=Environments.EID AND Presets.PID=Projectiles.PID AND Presets.MID=Motion.MID AND 
            Presets.name=?""",
                      [record_name])
            record = c.fetchall()[0]
            record_drag = bool(record[8])
            v_label.config(text=record[0])
            ele_label.config(text=record[1])
            azi_label.config(text=record[2])
            x_label.config(text=record[3])
            y_label.config(text=record[4])
            z_label.config(text=record[5])
            g_label.config(text=record[6])

            if record_drag:
                drag_label.config(text="True")
                m_label.config(text=record[9])
                rho_label.config(text=record[7])
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

        preview_button = Button(db_view_frame, text="Preview", bg=colours["but_bg"], fg=colours["text"],
                                command=previewRecord, borderwidth=0, disabledforeground=colours["text"])
        preview_button.place(x=250, y=120)
        chosen_record = StringVar(database_win)
        chosen_record.set("Select Preset")
        try:
            menu = OptionMenu(db_view_frame, chosen_record, *records)
        except TypeError:  # Runs if there are no records
            chosen_record.set("No Presets")
            records = [" "]
            menu = OptionMenu(db_view_frame, chosen_record, *records)
            menu.config(state="disabled", disabledforeground=colours["text"])
            preview_button.config(state="disabled")
        menu.config(borderwidth=0, fg=colours["text"], bg=colours["but_bg"])
        menu.place(x=100, y=120)

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
            label.place(x=200, y=170+count*20)

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
            label.place(x=430, y=170+count*20)

        CustomButton(db_view_frame, **style["button"], text="Load", width=10, command=loadRecord).place(x=600, y=220)
        Button(db_view_frame, **style["neg button"], text="Delete", width=10, command=deleteRecord).place(x=600, y=270)

    def loadDatabaseSaveFrame():
        def saveRecord():
            # Checks if name is unique
            c.execute("SELECT name FROM Presets WHERE name=?", [new_preset.get()])
            records = c.fetchall()
            if records:  # Checks if name is unique
                messagebox.showerror("Error", "Invalid input: name already in use")
                return
            if len(new_preset.get()) > 20:  # Checks if the name is too long
                messagebox.showerror("Error", "Invalid input: name must be at most 20 characters")
                return
            elif new_preset.get() == "":  # Checks if the field is empty
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
                values += [None] * 4

            # Checks for any empty fields
            if "" in values:
                messagebox.showerror("Error", "Empty fields")
                return

            # Checks for invalid inputs
            try:
                if drag:
                    values = list(map(float, values))
                else:
                    values[0:7] = list(map(float, values[0:7]))
            except ValueError:
                messagebox.showerror("Error", "Inputs must be numbers")
                return

            # Passes the values into the function verifyInputs to check validity
            valid = verifyInputs(*values)
            if not valid:
                return

            motion_record = values[0:6]
            environment_record = values[6:9:2]
            projectile_record = values[9:]

            # Finds environment id
            c.execute("SELECT EID FROM Environments WHERE (gravity,air_density) IS (?,?)",
                      environment_record)
            eid = c.fetchall()
            if not eid:
                c.execute("INSERT INTO Environments (gravity,air_density) VALUES (?,?)",
                          tuple(environment_record))
                db.commit()
                c.execute("SELECT EID FROM Environments WHERE (gravity,air_density) IS (?,?)",
                          environment_record)
                eid = c.fetchall()[0][0]
            else:
                eid = eid[0][0]

            # Finds projectile id
            c.execute("SELECT PID FROM Projectiles WHERE (mass,drag_coefficient,area) IS (?,?,?)",
                      projectile_record)
            pid = c.fetchall()
            if not pid:
                c.execute("INSERT INTO Projectiles (mass,drag_coefficient,area) VALUES (?,?,?)",
                          tuple(projectile_record))
                db.commit()
                c.execute("SELECT PID FROM Projectiles WHERE (mass,drag_coefficient,area) IS (?,?,?)",
                          projectile_record)
                pid = c.fetchall()[0][0]
            else:
                pid = pid[0][0]

            # Finds motion id
            c.execute("SELECT MID FROM Motion WHERE (velocity,ele_angle,azi_angle,x,y,z) IS (?,?,?,?,?,?)",
                      motion_record)
            mid = c.fetchall()
            if not mid:
                c.execute("INSERT INTO Motion (velocity,ele_angle,azi_angle,x,y,z) VALUES (?,?,?,?,?,?)",
                          tuple(motion_record))
                db.commit()
                c.execute("SELECT MID FROM Motion WHERE (velocity,ele_angle,azi_angle,x,y,z) IS (?,?,?,?,?,?)",
                          motion_record)
                mid = c.fetchall()[0][0]
            else:
                mid = mid[0][0]

            c.execute("SELECT name FROM Presets WHERE (EID,PID,MID)=(?,?,?)", [eid, pid, mid])
            repeats = c.fetchall()
            if not repeats:
                c.execute("INSERT INTO Presets (name,drag,EID,PID,MID) VALUES (?,?,?,?,?)",
                          (new_preset.get(), drag, eid, pid, mid))
                db.commit()
                messagebox.showinfo("Preset Saved", "Preset successfully saved")
            else:
                messagebox.showerror("Error", f"Invalid value/s: record already exists under '{repeats[0][0]}'")
                return

        new_preset = StringVar(database_win)
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


# Database
db = sqlite3.connect("presets.db")  # Connects to file presets.db
db.execute("PRAGMA foreign_keys = ON")  # Enables foreign keys
c = db.cursor()

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

with open("themes.json", "r") as file:  # Opens the JSON file
    themes = json.load(file)  # Loads all themes to dictionary
colours = {"neg": "#D62F2F", "pos": "#109110"}  # Stores the current theme
colours.update(themes["Dark"])  # Sets the current theme to dark
current_theme = StringVar(value="Dark")  # Variable to store the current theme
colourblind_mode = BooleanVar(value=False)  # Boolean value for if colourblind mode is active
style = loadTheme()

root.config(bg=colours["but_bg"])

# tools_frame = Frame(root)
input_frame = Frame(root)
output_frame = Frame(root)
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
compare_drag = BooleanVar(value=False)

# Results
position = StringVar(value="__________, __________, __________")
velocity = StringVar(value="__________")
displacement = StringVar(value="__________")
landing_time = StringVar(value="__________")
max_height = StringVar(value="__________")
time = StringVar(value="__________")

loadToolsFrame()
loadInputFrame()
loadOutputFrame()
loadGraphFrame()

root.mainloop()
