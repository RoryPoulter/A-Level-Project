# The main body of code
# Created: 04/10/23
# Last edited: 30/11/23

import projectile  # Projectile calculations
from tkinter import *  # GUI
from tkinter import messagebox  # Error messages
import sqlite3  # Database
import json  # Themes
import ctypes


# Checks if the data fall within the correct ranges
def verifyInputs(u: float, ele_angle: float, azi_angle: float, x: float, y: float, z: float, g: float, drag=False,
                 m: float = None, rho: float = None, cd: float = None, area: float = None) -> bool:
    if u <= 0:
        messagebox.showerror("Error", "Invalid input: velocity must fall within the range: 0 < u")
        return False
    if ele_angle < 0:
        messagebox.showerror("Error", "Invalid input: elevation angle must fall within the range: 0 ≤ θe")
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
    tools_frame = Frame(root, bg=colours["bg"])
    tools_frame.place(x=0, y=0, width=1000, height=26)
    Button(tools_frame, bg=colours["but_bg"], fg=colours["text"], text="Settings", command=openSettingsWindow,
           borderwidth=0, font=("Calibri", 16)).pack(side=LEFT)
    Button(tools_frame, bg=colours["neg"], fg="#FFFFFF", text="X", command=loadMenuFrame, borderwidth=0,
           font=("Calibri", 16)).pack(side=RIGHT)


def loadMenuFrame():
    closeCurrentFrame()
    current_frame.set("menu")
    menu_frame.config(bg=colours["bg"])
    menu_frame.place(x=0, y=26, width=1000, height=574)
    Label(menu_frame, bg=colours["bg"], fg=colours["text"], text="3D Projectile Simulator",
          font=("Calibri", 20)).place(relx=0.5, y=75, anchor=CENTER)
    Button(menu_frame, bg=colours["but_bg"], fg=colours["text"], text="Info", command=loadInfoFrame, width=10,
           borderwidth=0, font=("Calibri", 14)).place(relx=0.25, rely=0.6, anchor=CENTER)
    Button(menu_frame, bg=colours["but_bg"], fg=colours["text"], text="Sim", command=loadSimFrame, width=10,
           borderwidth=0, font=("Calibri", 14)).place(relx=0.75, rely=0.6, anchor=CENTER)


def loadInfoFrame():
    closeCurrentFrame()
    current_frame.set("info")
    info_frame.config(bg=colours["bg"])
    info_frame.place(x=0, y=26, width=1000, height=574)
    with open("definitions.txt", "r", encoding="utf-8") as file:
        for num, line in enumerate(file):
            definition = line.strip()
            Label(info_frame, text=definition, bg=colours["bg"], fg=colours["text"],
                  font=("Calibri", 14)).place(x=20, y=50 * (num + 1))


def loadSimFrame():
    def displayResults():
        position_label.config(text=position.get())
        velocity_label.config(text=velocity.get() + "m/s")
        displacement_label.config(text=displacement.get() + "m")
        landing_time_label.config(text=landing_time.get() + "s")
        max_height_label.config(text=max_height.get() + "m")
        time_label.config(text=time.get() + "s")

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

        # Creates the objects using the values
        if drag:
            proj = projectile.ProjectileDrag(*values, colour=colours["pos"])
        else:
            proj = projectile.ProjectileNoDrag(*values, colour=colours["neg"])
        dt = 0.01
        # Updates the position until it is on the ground
        while proj.pos[2] >= 0:
            proj.move(dt)

        if drag:
            position.set("\n".join(str(round(x, 5)) for x in proj.pos))
            landing_time.set(str(round(proj.time, 5)) + "s")
        else:
            position.set("\n".join(str(round(x, 5)) for x in proj.landing_pos))
            landing_time.set(str(round(proj.landing_time, 5)) + "s")
        velocity.set(str(round(projectile.mag(proj.v), 5)) + "m/s")
        displacement.set(str(round(proj.calcDisplacement(), 5)) + "m")
        max_height.set(str(round(proj.max_h, 5)) + "m")
        time.set(str(round(proj.max_t, 5)) + "s")
        displayResults()

        # Loads the 3D scatter graph
        proj.displayPath()

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

    closeCurrentFrame()
    current_frame.set("sim")
    sim_frame.config(bg=colours["bg"])
    sim_frame.place(x=0, y=26, width=1000, height=574)

    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Velocity [m/s]:", font=("Calibri", 14),
          width=16, anchor="e").place(x=30, y=100)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Elevation Angle [°]:", font=("Calibri", 14),
          width=16, anchor="e").place(x=30, y=150)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Azimuth Angle [°]:", font=("Calibri", 14),
          width=16, anchor="e").place(x=30, y=200)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="x:", font=("Calibri", 14),
          width=16, anchor="e").place(x=30, y=250)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="y:", font=("Calibri", 14),
          width=16, anchor="e").place(x=30, y=300)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="z:", font=("Calibri", 14),
          width=16, anchor="e").place(x=30, y=350)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Gravity [m/s²]:", font=("Calibri", 14),
          width=16, anchor="e").place(x=30, y=400)

    Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
          textvariable=initial_velocity).place(x=200, y=100)
    Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
          textvariable=elevation_angle).place(x=200, y=150)
    Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
          textvariable=azimuth_angle).place(x=200, y=200)
    Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
          textvariable=x0).place(x=200, y=250)
    Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
          textvariable=y0).place(x=200, y=300)
    Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
          textvariable=z0).place(x=200, y=350)
    Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
          textvariable=gravity).place(x=200, y=400)

    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Mass [kg]:", font=("Calibri", 14),
          width=16, anchor="e").place(x=370, y=100)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Air Density [kg/m³]:", font=("Calibri", 14),
          width=16, anchor="e").place(x=370, y=150)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Drag Coefficient:", font=("Calibri", 14),
          width=16, anchor="e").place(x=370, y=200)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Surface Area [m²]:", font=("Calibri", 14),
          width=16, anchor="e").place(x=370, y=250)

    if drag:
        m_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                        textvariable=mass)
        rho_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                          textvariable=air_density)
        cd_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                         textvariable=drag_coefficient)
        a_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                        textvariable=surface_area)
        drag_button = Button(sim_frame, bg=colours["pos"], fg="#ffffff", text="Drag", command=toggle, width=15,
                             font=("Calibri", 16), borderwidth=0)
    else:
        m_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                        state="disabled", textvariable=mass)
        rho_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                          state="disabled", textvariable=air_density)
        cd_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                         state="disabled", textvariable=drag_coefficient)
        a_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 14), width=10,
                        state="disabled", textvariable=surface_area)
        drag_button = Button(sim_frame, bg=colours["neg"], fg="#ffffff", text="No Drag", command=toggle, width=15,
                             font=("Calibri", 14), borderwidth=0)

    m_entry.place(x=540, y=100)
    rho_entry.place(x=540, y=150)
    cd_entry.place(x=540, y=200)
    a_entry.place(x=540, y=250)
    drag_button.place(x=450, y=320)

    Button(sim_frame, bg=colours["but_bg"], fg=colours["text"], text="Run", font=("Calibri", 14), borderwidth=0,
           width=15, command=run).place(x=450, y=390)

    Label(sim_frame, text="Position:", bg=colours["bg"], fg=colours["text"], font=("Calibri", 14), width=12,
          anchor="e").place(x=700, y=100)
    Label(sim_frame, text="Final Velocity:", bg=colours["bg"], fg=colours["text"], font=("Calibri", 14), width=12,
          anchor="e").place(x=700, y=190)
    Label(sim_frame, text="Displacement:", bg=colours["bg"], fg=colours["text"],
          font=("Calibri", 14), width=12, anchor="e").place(x=700, y=220)
    Label(sim_frame, text="Landing Time:", bg=colours["bg"], fg=colours["text"],
          font=("Calibri", 14), width=12, anchor="e").place(x=700, y=250)
    Label(sim_frame, text="Max Height:", bg=colours["bg"], fg=colours["text"], font=("Calibri", 14),
          width=12, anchor="e").place(x=700, y=280)
    Label(sim_frame, text="Time:", bg=colours["bg"], fg=colours["text"], font=("Calibri", 14), width=12,
          anchor="e").place(x=700, y=310)

    position_label = Label(sim_frame, bg=colours["bg"], fg=colours["text"], font=("Calibri", 14), textvariable=position)
    position_label.place(x=825, y=100)
    velocity_label = Label(sim_frame, bg=colours["bg"], fg=colours["text"], font=("Calibri", 14), textvariable=velocity)
    velocity_label.place(x=825, y=190)
    displacement_label = Label(sim_frame, bg=colours["bg"], fg=colours["text"], font=("Calibri", 14),
                               textvariable=displacement)
    displacement_label.place(x=825, y=220)
    landing_time_label = Label(sim_frame, bg=colours["bg"], fg=colours["text"], font=("Calibri", 14),
                               textvariable=landing_time)
    landing_time_label.place(x=825, y=250)
    max_height_label = Label(sim_frame, bg=colours["bg"], fg=colours["text"], font=("Calibri", 14),
                             textvariable=max_height)
    max_height_label.place(x=825, y=280)
    time_label = Label(sim_frame, bg=colours["bg"], fg=colours["text"], font=("Calibri", 14), textvariable=time)
    time_label.place(x=825, y=310)

    Button(sim_frame, bg=colours["but_bg"], fg=colours["text"], text="Presets", borderwidth=0, font=("Calibri", 14),
           width=15, command=openDatabaseWindow).place(x=450, y=460)


def openSettingsWindow():
    global settings_win
    settings_win = Toplevel(root)
    settings_win.attributes('-topmost', 'true')
    settings_win.resizable(False, False)
    settings_win.title("Settings")
    settings_win.geometry("400x250")
    settings_win.grab_set()
    loadSettingsFrame(settings_win)


def loadSettingsFrame(win: Tk):
    settings_frame = Frame(win, bg=colours["bg"])
    settings_frame.place(x=0, y=0, width=400, height=250)

    Label(settings_frame, bg=colours["bg"], fg=colours["text"], text="Settings", font=("Calibri", 18)).place(relx=0.5,
                                                                                                             y=30,
                                                                                                             anchor=CENTER)
    Label(settings_frame, bg=colours["bg"], fg=colours["text"], text="Theme:", font=("Calibri", 14)).place(x=50, y=70)

    menu = OptionMenu(settings_frame, current_theme, *themes)
    menu.config(bg=colours["but_bg"], fg=colours["text"], borderwidth=0, highlightbackground=colours["bg"],
                font=("Calibri", 12), width=10, activeforeground=colours["text"], activebackground=colours["but_bg"])
    menu.place(x=120, y=70)

    Checkbutton(settings_frame, text="Colourblind Mode", variable=colourblind_mode,
                bg=colours["bg"], activebackground=colours["bg"],
                activeforeground=colours["text"], font=("Calibri", 16)).place(x=50, y=120)

    Button(settings_frame, bg=colours["but_bg"], fg=colours["text"], text="Confirm", command=updateScheme,
           borderwidth=0).pack(anchor="s", side=RIGHT)


def updateScheme():
    colours.update(themes[current_theme.get()])

    if colourblind_mode.get():
        colours.update({"neg": "#FF8700", "pos": "#1E78E5"})
    else:
        colours.update({"neg": "#D62F2F", "pos": "#109110"})

    loadFrames()


def loadFrames():
    frames = {
        "menu": loadMenuFrame,
        "info": loadInfoFrame,
        "sim": loadSimFrame
    }
    loadToolsFrame()
    loadSettingsFrame(settings_win)
    frames[current_frame.get()]()


def closeCurrentFrame():
    close = {
        "menu": menu_frame.place_forget,
        "info": info_frame.place_forget,
        "sim": sim_frame.place_forget
    }
    close[current_frame.get()]()


def openDatabaseWindow():

    def loadDatabaseMenuFrame():
        db_menu_frame = Frame(database_win, bg=colours["bg"])
        db_menu_frame.place(x=0, y=26, width=800, height=374)
        Label(db_menu_frame, bg=colours["bg"], fg=colours["text"], text="Manage Presets", font=("Calibri", 20)).place(
            relx=0.5, y=50, anchor=CENTER)

        Button(db_menu_frame, bg=colours["but_bg"], fg=colours["text"], text="Save Preset", borderwidth=0, width=12,
               font=("Calibri", 14), command=loadDatabaseSaveFrame).place(x=250, y=250, anchor=CENTER)
        Button(db_menu_frame, bg=colours["but_bg"], fg=colours["text"], text="View Presets", borderwidth=0, width=12,
               font=("Calibri", 14), command=loadDatabaseViewFrame).place(x=550, y=250, anchor=CENTER)

    def loadDatabaseViewFrame():
        def deleteRecord():
            record_name = chosen_record.get()
            if record_name == "Select Preset":
                return
            c.execute("DELETE FROM Presets WHERE name=?", [record_name])
            db.commit()
            records.remove(record_name)

        def loadRecord():
            global drag
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
            drag = bool(record[8])

            for value, variable in zip(record[:7], [initial_velocity, elevation_angle, azimuth_angle, x0, y0, z0, gravity]):
                variable.set(value=value)

            if drag:
                for value, variable in zip(record[8:], [air_density, mass, drag_coefficient, surface_area]):
                    variable.set(value=value)

            loadSimFrame()

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
            record_drag = bool(record[7])
            v_label.config(text=record[0])
            ele_label.config(text=record[1])
            azi_label.config(text=record[2])
            x_label.config(text=record[3])
            y_label.config(text=record[4])
            z_label.config(text=record[5])
            g_label.config(text=record[6])

            if record_drag:
                drag_label.config(text="True")
                m_label.config(text=record[8])
                rho_label.config(text=record[9])
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

        Label(db_view_frame, text="v [m/s]:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=120, y=170)
        Label(db_view_frame, text="θe [°]:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=120, y=190)
        Label(db_view_frame, text="θa [°]:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=120, y=210)
        Label(db_view_frame, text="x:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=120, y=230)
        Label(db_view_frame, text="y:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=120, y=250)
        Label(db_view_frame, text="z:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=120, y=270)
        Label(db_view_frame, text="g [m/s²]:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=120, y=290)

        v_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        ele_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        azi_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        x_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        y_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        z_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        g_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])

        for count, label in enumerate((v_label, ele_label, azi_label, x_label, y_label, z_label, g_label)):
            label.place(x=200, y=170+count*20)

        Label(db_view_frame, text="Drag:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=350, y=170)
        Label(db_view_frame, text="m [kg]:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=350, y=190)
        Label(db_view_frame, text="ρ [kg/m³]:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=350, y=210)
        Label(db_view_frame, text="C:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=350, y=230)
        Label(db_view_frame, text="A [m²]:", anchor="e", width=10, bg=colours["bg"], fg=colours["text"]).place(x=350, y=250)

        drag_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        m_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        rho_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        cd_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])
        a_label = Label(db_view_frame, bg=colours["bg"], fg=colours["text"])

        for count, label in enumerate((drag_label, m_label, rho_label, cd_label, a_label)):
            label.place(x=430, y=170+count*20)

        Button(db_view_frame, text="Load", bg=colours["but_bg"], fg=colours["text"], borderwidth=0,
               font=("Calibri", 14), width=10, command=loadRecord).place(x=600, y=220)
        Button(db_view_frame, text="Delete", bg=colours["neg"], fg="#FFFFFF", borderwidth=0,
               font=("Calibri", 14), width=10, command=deleteRecord).place(x=600, y=270)

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
                    values = list(map(lambda x: float(x), values))
                else:
                    values[0:7] = list(map(lambda x: float(x), values[0:7]))
            except ValueError:
                messagebox.showerror("Error", "Inputs must be numbers")
                return

            # Passes the values into the function verifyInputs to check validity
            valid = verifyInputs(*values)
            if not valid:
                return

            motion_record = values[0:6]
            environment_record = values[7:9]
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
            else:
                messagebox.showerror("Error", f"Invalid value/s: record already exists under '{repeats[0][0]}'")
                return

        new_preset = StringVar(database_win)
        db_save_frame = Frame(database_win, bg=colours["bg"])
        db_save_frame.place(x=0, y=26, width=800, height=374)
        Label(db_save_frame, bg=colours["bg"], fg=colours["text"], text="Save Preset",
              font=("Calibri", 20)).place(relx=0.5, y=50, anchor=CENTER)

        Label(db_save_frame, bg=colours["bg"], fg=colours["text"], text="Name:",
              font=("Calibri", 14)).place(relx=0.5, y=150, anchor=CENTER)
        Entry(db_save_frame, bg=colours["but_bg"], fg=colours["text"],
              textvariable=new_preset, font=("Calibri", 14)).place(relx=0.5, y=175, anchor=CENTER)
        Button(db_save_frame, bg=colours["but_bg"], fg=colours["text"], text="Save Preset",
               command=saveRecord, borderwidth=0, font=("Calibri", 14)).place(relx=0.5, y=225, anchor=CENTER)

    database_win = Toplevel(root)
    database_win.resizable(False, False)
    database_win.title("Database")
    database_win.geometry("800x400")
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

root = Tk()  # Creates the window
root.title("Main window")  # Sets the window title
root.geometry("1000x600")  # Sets the window dimensions
root.resizable(False, False)  # Prevents user from adjusting window size

# The frames used on the window
menu_frame = Frame(root)
info_frame = Frame(root)
sim_frame = Frame(root)

# Loads the data in the file themes.json into a dictionary
with open("themes.json", "r") as file:
    themes = json.load(file)
colours = {}
colours.update(themes["Dark"])  # Sets the current theme to dark
current_theme = StringVar(value="Dark")  # Variable to store the current theme
colourblind_mode = BooleanVar(value=False)  # Boolean value for if colourblind mode is active
current_frame = StringVar(value="menu")  # Variable to store the current open frame

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

# Results
position = StringVar(value="__________\n__________\n__________")
velocity = StringVar(value="__________m/s")
displacement = StringVar(value="__________m")
landing_time = StringVar(value="__________s")
max_height = StringVar(value="__________m")
time = StringVar(value="__________s")

loadToolsFrame()  # Loads the toolbar
loadMenuFrame()  # Loads the menu

root.mainloop()  # Runs the program
