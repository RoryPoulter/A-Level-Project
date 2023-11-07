# The main body of code
# Created: 04/10/23
# Last edited: 07/10/23

import projectile  # Projectile calculations
from tkinter import *  # GUI
import sqlite3  # Database


def run():
    global drag


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
    current_frame.set("menu")
    menu_frame = Frame(root, bg=colours["bg"])
    menu_frame.place(x=0, y=26, width=1000, height=574)
    Button(menu_frame, bg=colours["but_bg"], fg=colours["text"], text="Info", command=loadInfoFrame, width=10,
           height=2, borderwidth=0).place(relx=0.2, rely=0.6)
    Button(menu_frame, bg=colours["but_bg"], fg=colours["text"], text="Sim", command=loadSimFrame, width=10,
           height=2, borderwidth=0).place(relx=0.7, rely=0.6)


def loadInfoFrame():
    current_frame.set("info")
    info_frame = Frame(root, bg=colours["bg"])
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

    current_frame.set("sim")
    sim_frame = Frame(root, bg=colours["bg"])
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

    u_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
    u_entry.place(x=240, y=100)
    ele_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
    ele_entry.place(x=240, y=150)
    azi_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
    azi_entry.place(x=240, y=200)
    x_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
    x_entry.place(x=240, y=250)
    y_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
    y_entry.place(x=240, y=300)
    z_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
    z_entry.place(x=240, y=350)
    g_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
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
        m_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
        rho_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
        cd_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
        a_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10)
        drag_button = Button(sim_frame, bg=colours["pos"], fg="#ffffff", text="Drag", command=toggle, width=15,
                             font=("Calibri", 16), borderwidth=0)
    else:
        m_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                        state="disabled")
        rho_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                          state="disabled")
        cd_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                         state="disabled")
        a_entry = Entry(sim_frame, bg=colours["but_bg"], fg=colours["text"], font=("Calibri", 16), width=10,
                        state="disabled")
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
    settings_win.geometry("400x400")
    loadSettingsFrame(settings_win)


def loadSettingsFrame(win):
    settings_frame = Frame(win, bg=colours["bg"])
    settings_frame.place(x=0, y=0, width=400, height=400)

    Radiobutton(settings_frame, text="Dark Mode", variable=dark, value=True, bg=colours["bg"],
                activebackground=colours["bg"], activeforeground=colours["text"],
                font=("Calibri", 16)).place(x=50, y=50)

    Radiobutton(settings_frame, text="Light Mode", variable=dark, value=False, bg=colours["bg"],
                activebackground=colours["bg"], activeforeground=colours["text"],
                font=("Calibri", 16)).place(x=50, y=100)

    Checkbutton(settings_frame, text="Colourblind Mode", variable=colourblind_mode,
                bg=colours["bg"], activebackground=colours["bg"],
                activeforeground=colours["text"], font=("Calibri", 16)).place(x=50, y=150)

    Button(settings_frame, bg=colours["but_bg"], fg=colours["text"], text="Confirm", command=updateScheme).place(x=50,
                                                                                                                 y=350)


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


drag = False
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

current_frame = StringVar(value="menu")  # Variable to store the current open frame
dark = BooleanVar(value=True)  # Boolean value for if the theme is dark
colourblind_mode = BooleanVar(value=False)  # Boolean value for if colourblind mode is active

loadToolsFrame()
loadMenuFrame()

root.mainloop()
