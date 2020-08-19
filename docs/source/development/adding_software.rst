Adding Software
***************

1. Create an app config file
    ``mb_armada/app_configs/software.json``
2. Create an app path resolver
    ``mb_utils/path_resolver/resolver_templates/armada/apps/software/software_template.py``
3. Create a launch hook
    ``mb_armada/hooks/launchers/software_hook.py``
    3a. Optional: Create pythonpath directories to launch other software or plugins at startup
        ``mb_armada/hooks/launchers/apps/software/scripts``
        ``mb_armada/hooks/launchers/apps/software/plugins``
4. Add app icon to resources

Configs
=======

- An app config file should be placed in Armada's app_configs directory and should be named like this: ``software.json``.
- JSON file data

    {

        "working_dir": "dir_name",

        "extension": "ext"

    }

- working_dir: The folder name of the directory that the software typically saves to
    - Example: Maya's working_dir is called "scenes"
- "extension": Some programs can save in multiple file formats (binary, ascii). For these programs it's useful to restrict users to a single extension.
    - Example: Maya has binary and ascii formats for its save files.
    - Ascii is good for working files because things can become corrupt and having the ability to read and edit the file by hand will allow you to recover documents
        - Binary isn't editable, but the file size is smaller. This makes it a good format for asset exporting.

Resolver Templates
==================

- A template file in mb_util's resolver templates path that contains all the extra directories required for a software
    - Example: Maya's working directory, scenes, has many sibling directories such as images, assets, renderData, etc.
    - With these templates you can add your own custom directories on top of the defaults.



Launch Hooks
============

- A launch hook runs the software and sets all the necessary environment variables from within the hook
    - Some software will allow you to add paths to
        - If so add a software folder to hook/app and add any necessary folders such as "scripts" or "plugins"

- You can create your own environment variables here
