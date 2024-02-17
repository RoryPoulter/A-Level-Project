﻿# A-Level-Project
Python program to simulate projectile motion in 3 dimensions.\
Developed for my Computer Science A-Level project.

## Installation
### Automatic Installation
Run the file `.build/setup.cmd`

### Manual Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
```bash
pip install -r /path/to/requiremnets.txt
```
Once the libraries have been installed, run the file `src/main.py`

## Usage
This program allows the user to simulate projectile motion based on chosen initial conditions.
Includes definitions of key terms which are read from an external .txt file.
The effects of drag can be included/excluded, or both to show how it affects a projectile.

The program uses tkinter for the main GUI, and matplotlib to display the results. 
The appearance of the GUI can be changed by toggling colourblind mode and changing the theme.
The themes are stored in an external JSON file.

![themes-demo](https://github.com/RoryPoulter/A-Level-Project/assets/118304377/254f73dc-8836-476d-a3e6-a40aecf5c6bf)

The program uses NumPy for the vector calculations. Due to the nature of the drag calculations, results 
including drag are only approximations.

### Presets
The program allows users to save presets to an external .db file. The GUI features a window
to manage the presets.\
The values can be previewed in the preset window and loaded into the entry fields in the main
window.

![presets-demo](https://github.com/RoryPoulter/A-Level-Project/assets/118304377/01377cf2-ab31-4103-9f9b-6bb7b1ea2410)


## Development
Written in [Python 3.10](https://www.python.org/downloads/).\
Development is finished.
