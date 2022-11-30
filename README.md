
# Source Execution


## Installation
Prepare your environment
```
python -m venv venv
venv\Scripts\activate

######### upgrade pip--- python.exe -m pip install --upgrade pip
pip install cx_freeze setuptools
pip install -e .
```
you might have an error in the end, no problem

## Running 
run the main app by
````
python app.py
````

# Building the executable
run
```
python setup.py build_exe
```

you find the executable at `.\build\exe.win-amd64-3.8\app.exe`

# Distribution
## Installer
* Install Inno Setup and compile `setup.iss`
* You find the installer in `.\Output`
* Distribute the installer
* Execute after installation the program via the start menu

## Zip Archive
* Archive the content and subfolder of the folder `.\build\exe.win-amd64-3.8`
* Distribute the zip archive
* Execute after extraction `app.exe` at the specified location





