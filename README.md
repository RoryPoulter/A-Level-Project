# A-Level-Project
Python program to simulate projectile motion in 3 dimensions.

Computer Science A-Level project.

This program allows the user to simulate projectile motion based on chosen initial conditions.
Includes definitions of key terms which are read from an external .txt file.
The effects of drag can be included/excluded to show how it affects a projectile.

The program uses tkinter for the main GUI, and matplotlib to display the results. 
The appearance of the GUI can be changed by toggling colourblind mode and changing the theme.
The themes are stored in an external JSON file.

The program uses NumPy for the vector calculations. Due to the nature of the drag calculations, results 
including drag are only approximations.

Presets for values can be stores in an external .db file to be loaded later.

Currently in development.
Future updates will include:
<ul>
    <li>Embed flight path in window
    <li>Additional themes
</ul>