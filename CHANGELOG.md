# CHANGELOG

## v1.1.1 [2024-02-21]
### Improvements
* Database can store option to compare paths

### Other changes
* Improved modularity of code
  * Created function to declare cursor and set up database
  * Created function to set up whole GUI
* Created `test/` directory

## v1.1 [2024-02-19]
### Improvements
* New file `config.json` to store GUI settings
  * Maintains the last used theme and if colourblind mode was active

### Bug Fixes
* Fixed issue with close button

## v1.0.3 [2024-02-17]
### Other Changes
* Updated documentation
  * Added comments to `setup.cmd`
  * Added `doc/` directory
  * Removed `Media/` directory

## v1.0.2 [2024-02-05]
### Bug Fixes
* Fixed logic error with elevation angle
  * Updated `definitions.txt` and error messages to include 90 degrees in range of accepted values

## v1.0.1 [2024-01-28]
### Improvements
* `setup.cmd` created for installing modules before running program for the first time
  * Before running the main program, run `setup.cmd`
  * Installs the modules listed in `requirements.txt`
  * Opens the program after modules have installed