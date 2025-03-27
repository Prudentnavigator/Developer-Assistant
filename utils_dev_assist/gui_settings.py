#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
gui_settings.py--This script is responsible for the appearance and scaling of
                 the DeveloperAssistant app.
'''

import json
import customtkinter as ctk
from utils_dev_assist.dev_assist_logging import app_log

logger = app_log(__name__)


def get_appearance_mode(menu: bool = False) -> ctk.set_appearance_mode:
    '''
    This function retrieves and sets appearance mode based from a
    configuration file, if the file does not exists then default will be
    set to 'System'.
    '''

    try:
        with open(".gui_config.cfg", "r", encoding="utf-8") as cfg:
            data = json.load(cfg)

            if menu:
                return data["theme"]

            logger.debug(" [SETTINGS] appearance mode -> set.")

            return ctk.set_appearance_mode(data["theme"])

    except FileNotFoundError:
        with open(".gui_config.cfg", "w", encoding="utf-8") as cfg:
            data = {"theme": "System"}
            cfg.write(json.dumps(data))

            logger.debug(" [SETTINGS] config file -> created!")

            return ctk.set_appearance_mode(data["theme"])


def get_color_theme() -> ctk.set_default_color_theme:
    '''
    Responsible for retrieving the default color theme for the GUI elements
    of the application specified in the 'dev_assist_theme.json' file.
    '''

    logger.debug(" [SETTINGS] color theme -> set.")

    return ctk.set_default_color_theme("assets/dev_assist_theme.json")


def change_appearance_mode(mode: str) -> ctk.set_appearance_mode:
    '''
    Changes the GUI appearance and stores the mode chosen in the config file.
    '''

    with open(".gui_config.cfg", "w", encoding="utf-8") as cfg:
        data = {"theme": mode}
        cfg.write(json.dumps(data))

    logger.debug(" [SETTINGS] appearance has been changed.")

    return ctk.set_appearance_mode(mode)


def change_scaling(new_scaling: str) -> ctk.set_widget_scaling:
    '''
    Changes the scale of the GUI.
    '''

    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    logger.debug(" [SETTINGS] app scale changed.")

    return ctk.set_widget_scaling(new_scaling_float)
