# A-Level-Project
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
### Settings
Resolution: 1920x1080\
Text scaling: 100%
### Simulation
The values can be input into text boxes.

To toggle if drag is included, tick the 'Drag' radiobutton. If you want to show both flight 
paths, tick the "Compare" radiobutton. Due to the nature of the drag calculations, results including drag are 
only approximations.

### GUI
The program uses tkinter for the main GUI, and matplotlib to display the results. 
The appearance of the GUI can be changed by toggling colourblind mode and changing the theme.
The themes are stored in an external JSON file.

![themes-demo](https://github.com/RoryPoulter/A-Level-Project/assets/118304377/254f73dc-8836-476d-a3e6-a40aecf5c6bf)

### Presets
The program allows users to save presets to an external .db file. The GUI features a window
to manage the presets.
![presets-demo](https://github.com/RoryPoulter/A-Level-Project/assets/118304377/01377cf2-ab31-4103-9f9b-6bb7b1ea2410)

#### Saving presets
* Enter the values into the text boxes on the main window
* Press the save icon
* Press the 'Save Preset' button
* Enter the preset name (must be unique and under 20 characters)
* Press 'Save'
* A pop-up will be displayed if successful

#### Previewing presets
* Press the save icon
* Press the 'View Presets' button
* Select the preset from the dropdown
* Press the 'Preview' button

#### Loading presets
* Press the save icon
* Press the 'View Presets' button
* Select the preset from the dropdown
* Press the 'Load' button
* The values will be automatically copied into the text boxes

#### Deleting presets
* Press the save icon
* Press the 'View Presets' button
* Select the preset from the dropdown
* Press the 'Delete' button
* A pop-up will be displayed if successful




## Roadmap
Written in [Python 3.10](https://www.python.org/downloads/).\
Future updates will include:
* Results for comparing projectiles
* Code overhaul to make future development easier
* Theme editor to create and save custom themes
* Full error diagnosis for input validation
* Button to reset graph