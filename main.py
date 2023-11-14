# The main body of code
# Created: 04/10/23
# Last edited: 10/11/23

import projectile  # Projectile calculations
from tkinter import *  # GUI
from tkinter import messagebox
import sqlite3  # Database


def verifyInputs(u: float, ele_angle: float, azi_angle: float, x: float, y: float, z: float, g: float, drag=False,
                 m: float = None, rho: float = None, cd: float = None, area: float = None) -> bool:
    message = "Invalid input: "
    # Checks if the data fall within the correct ranges
    error = "must fall within the range: "
    if u <= 0:
        messagebox.showerror("Error", message + "velocity " + error + "0 < u")
        return False
    if ele_angle < 0:
        messagebox.showerror("Error", message + "elevation angle " + error + "0 ≤ θe")
        return False
    if azi_angle < 0 or azi_angle >= 360:
        messagebox.showerror("Error", message + "azimuth angle " + error + "0 ≤ θa < 360")
        return False
    if x < 0:
        messagebox.showerror("Error", message + "x " + error + "0 ≤ x")
        return False
    if y < 0:
        messagebox.showerror("Error", message + "y " + error + "0 ≤ y")
        return False
    if z < 0:
        messagebox.showerror("Error", message + "z " + error + "0 ≤ z")
        return False
    if g <= 0:
        messagebox.showerror("Error", message + "g " + error + "0 < g")
        return False

    if drag:
        if m <= 0:
            messagebox.showerror("Error", message + "mass " + error + "0 < m")
            return False
        if rho <= 0:
            messagebox.showerror("Error", message + "air density " + error + "0 < ρ")
            return False
        if cd <= 0 or cd > 1:
            messagebox.showerror("Error", message + "drag coefficient " + error + "0 < cd ≤ 1")
            return False
        if area <= 0:
            messagebox.showerror("Error", message + "surface area " + error + "0 < A")
            return False

    return True


def run():
    global drag

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

    if "" in values:
        messagebox.showerror("Error", "Empty fields")
        return
    try:
        values = list(map(lambda x: float(x), values))
    except ValueError:
        messagebox.showerror("Error", "Inputs must be numbers")
        return

    if drag:
        valid = verifyInputs(*values[0:6], drag, *values[6:])
    else:
        valid = verifyInputs(*values)

    if not valid:
        return

    if drag:
        proj = projectile.ProjectileDrag(*values)
    else:
        proj = projectile.ProjectileNoDrag(*values)
    dt = 0.01
    while proj.pos[2] >=0:
        proj.move(dt)
    proj.displayPath()


def loadToolsFrame():
    tools_frame = Frame(root, bg=colours["bg"])
    tools_frame.place(x=0, y=0, width=1000, height=26)
    Button(tools_frame, bg=colours["but_bg"], fg=colours["text"], text="Settings", command=openSettingsWindow,
           borderwidth=0, font=("Calibri", 16)).pack(side=LEFT)
    Button(tools_frame, bg=colours["neg"], fg="#FFFFFF", text="X", command=loadMenuFrame, borderwidth=0,
           font=("Calibri", 16)).pack(
        side=RIGHT)
    Button(tools_frame, bg=colours["but_bg"], fg=colours["text"], text="DB", borderwidth=0, font=("Calibri", 16)).pack(
        side=LEFT, padx=2)


def loadMenuFrame():
    closeCurrentFrame()
    current_frame.set("menu")
    menu_frame.place(x=0, y=26, width=1000, height=574)
    Button(menu_frame, bg=colours["but_bg"], fg=colours["text"], text="Info", command=loadInfoFrame, width=10,
           height=2, borderwidth=0).place(relx=0.2, rely=0.6)
    Button(menu_frame, bg=colours["but_bg"], fg=colours["text"], text="Sim", command=loadSimFrame, width=10,
           height=2, borderwidth=0).place(relx=0.7, rely=0.6)


def loadInfoFrame():
    closeCurrentFrame()
    current_frame.set("info")
    info_frame.place(x=0, y=26, width=1000, height=574)
    Label(info_frame, bg=colours["bg"], fg=colours["text"], text="This is a test", font=("Calibri", 16)).place(x=260,
                                                                                                               y=150)


def loadSimFrame():
    def toggle():
        global drag
        if drag_button.config("text")[-1] == "No Drag":
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
    sim_frame.place(x=0, y=26, width=1000, height=574)

    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Velocity [m/s]:", font=("Calibri", 16),
          width=16, anchor="e").place(x=50, y=100)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Elevation Angle [°]:", font=("Calibri", 16),
          width=16, anchor="e").place(x=50, y=150)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Azimuth Angle [°]:", font=("Calibri", 16),
          width=16, anchor="e").place(x=50, y=200)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="x:", font=("Calibri", 16),
          width=16, anchor="e").place(x=50, y=250)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="y:", font=("Calibri", 16),
          width=16, anchor="e").place(x=50, y=300)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="z:", font=("Calibri", 16),
          width=16, anchor="e").place(x=50, y=350)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Gravity [m/s²]:", font=("Calibri", 16),
          width=16, anchor="e").place(x=50, y=400)

    u_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                    textvariable=initial_velocity)
    u_entry.place(x=240, y=100)
    ele_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                      textvariable=elevation_angle)
    ele_entry.place(x=240, y=150)
    azi_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                      textvariable=azimuth_angle)
    azi_entry.place(x=240, y=200)
    x_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                    textvariable=x0)
    x_entry.place(x=240, y=250)
    y_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                    textvariable=y0)
    y_entry.place(x=240, y=300)
    z_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                    textvariable=z0)
    z_entry.place(x=240, y=350)
    g_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                    textvariable=gravity)
    g_entry.place(x=240, y=400)

    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Mass [kg]:", font=("Calibri", 16),
          width=16, anchor="e").place(x=450, y=100)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Air Density [kg/m³]:", font=("Calibri", 16),
          width=16, anchor="e").place(x=450, y=150)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Drag Coefficient:", font=("Calibri", 16),
          width=16, anchor="e").place(x=450, y=200)
    Label(sim_frame, bg=colours["bg"], fg=colours["text"], text="Surface Area [m²]:", font=("Calibri", 16),
          width=16, anchor="e").place(x=450, y=250)

    if drag:
        m_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                        textvariable=mass)
        rho_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                          textvariable=air_density)
        cd_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                         textvariable=drag_coefficient)
        a_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                        textvariable=surface_area)
        drag_button = Button(sim_frame, bg=colours["pos"], fg="#ffffff", text="Drag", command=toggle, width=15,
                             font=("Calibri", 16), borderwidth=0)
    else:
        m_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                        state="disabled", textvariable=mass)
        rho_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                          state="disabled", textvariable=air_density)
        cd_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                         state="disabled", textvariable=drag_coefficient)
        a_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                        state="disabled", textvariable=surface_area)
        drag_button = Button(sim_frame, bg=colours["neg"], fg="#ffffff", text="No Drag", command=toggle, width=15,
                             font=("Calibri", 16), borderwidth=0)

    m_entry.place(x=640, y=100)
    rho_entry.place(x=640, y=150)
    cd_entry.place(x=640, y=200)
    a_entry.place(x=640, y=250)
    drag_button.place(x=550, y=320)

    Button(sim_frame, bg=colours["but_bg"], fg=colours["text"], text="Run", font=("Calibri", 16), borderwidth=0,
           width=15, command=run).place(x=550, y=390)


def openSettingsWindow():
    global settings_win
    settings_win = Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("400x250")
    loadSettingsFrame(settings_win)


def loadSettingsFrame(win):
    settings_frame = Frame(win, bg=colours["bg"])
    settings_frame.place(x=0, y=0, width=400, height=250)

    Radiobutton(settings_frame, text="Dark Mode", variable=dark, value=True, bg=colours["bg"],
                activebackground=colours["bg"], activeforeground=colours["text"],
                font=("Calibri", 16)).place(x=50, y=50)

    Radiobutton(settings_frame, text="Light Mode", variable=dark, value=False, bg=colours["bg"],
                activebackground=colours["bg"], activeforeground=colours["text"],
                font=("Calibri", 16)).place(x=50, y=100)

    Checkbutton(settings_frame, text="Colourblind Mode", variable=colourblind_mode,
                bg=colours["bg"], activebackground=colours["bg"],
                activeforeground=colours["text"], font=("Calibri", 16)).place(x=50, y=150)

    Button(settings_frame, bg=colours["but_bg"], fg=colours["text"], text="Confirm", command=updateScheme,
           borderwidth=0).pack(anchor="s", side=RIGHT)


def updateScheme():
    if dark.get():
        colours["bg"] = "#2E3142"
        colours["text"] = "#FFFFFF"
        colours["but_bg"] = "#555F70"
    else:
        colours["bg"] = "#F2F2F2"
        colours["text"] = "#000000"
        colours["but_bg"] = "#BFBFBF"

    if colourblind_mode.get():
        colours["neg"] = "#FF8700"
        colours["pos"] = "#1E78E5"
    else:
        colours["pos"] = "#109110"
        colours["neg"] = "#D62F2F"

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


colours = {
    "bg": "#2E3142",
    "text": "#FFFFFF",
    "but_bg": "#555F70",
    "neg": "#D62F2F",
    "pos": "#109110",
}

root = Tk()  # Creates the window
root.title("Main window")  # Sets the window title
root.geometry("1000x600")  # Sets the window dimensions
root.resizable(False, False)  # Prevents user from adjusting window size

menu_frame = Frame(root, bg=colours["bg"])
info_frame = Frame(root, bg=colours["bg"])
sim_frame = Frame(root, bg=colours["bg"])

current_frame = StringVar(value="menu")  # Variable to store the current open frame
dark = BooleanVar(value=True)  # Boolean value for if the theme is dark
colourblind_mode = BooleanVar(value=False)  # Boolean value for if colourblind mode is active

drag = False
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

loadToolsFrame()
loadMenuFrame()

root.mainloop()
