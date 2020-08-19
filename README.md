![Release](https://github.com/mikebourbeauart/mb-armada/workflows/Release/badge.svg)

![alt text](https://github.com/mikebourbeauart/mb-armada/blob/feature/lazy-loading/resources/help/cover_full.png?raw=true)

An art asset pipeline for artists

Artists
======
*Getting started:*
---------------

1. Download the latest release of Armada Pipeline (zip file) [here](https://github.com/mikebourbeauart/mb-armada/releases)
2. Extract it to a safe place on your hard drive
3. Before running the .exe file make sure to edit the config.json file in the configs folder (details for setup below)
4. Double click 'Armada Pipeline.exe'

*Setting up the config.json*
-----------------------

- The config.json file contains user-specific data and follows [json syntax](https://www.w3schools.com/js/js_json_syntax.asp). This process will be replaced with a GUI setup in the future, but for now artists will need to manually edit this file.

- ***IMPORTANT:*** You must wrap all values in double quotes (""), mind your commas at the end of the lines (exclude commas for the last value), and make sure your path slashes are forward facing!

- Example values: 

        "ARMADA_DEBUG": "1",
        "ARMADA_MOUNT_PREFIX": "path/to/your/pipeline/root",
        "ARMADA_STUDIO": "who-do-you-work-for",
        "ARMADA_SITE": "where-are-you-working-from",
        "ARMADA_MAYA_LOCATION": "C:/Program Files/Autodesk", 
        "ARMADA_BLENDER_LOCATION": "C:/Program Files"
	
- Values explained:

    - **ARMADA_DEBUG** - Determines what prints out to the console. You should keep it set to 1 in case somethign breaks. Any errors should be reported and include a copy of the console log. 
    - **ARMADA_MOUNT_PREFIX** - The root of the pipeline. This is where the magic happens. Point it to a cloud drive path for cloud access
    - **ARMADA_STUDIO** - This value is currently only used to name the log file.
    - **ARMADA_SITE** - This value is currently only used to name the log file.
    - **ARMADA_<APP>_LOCATION** - The example above shows the default locations for those software's root folders. It's common to install software in different locations so please make sure you point these values to the correct paths.

Developers
==========

- *Style:* PEP 8
- *Pull Requests:* master and develop branches only

Getting Started
---------------

Key Modules:

- armada
	- Armada's core package.
- launcher
	- The main file explorer from which all apps are launched.
- marina
	- A mini-launcher that manages software file iteration and resides within the software being utilized.
- atlantis
	- Asset manager that manages asset publishing, importing, and saving.
- utilsa
	- Contains utility classes like the custom logger
