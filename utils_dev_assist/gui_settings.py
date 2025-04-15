#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
gui_settings.py--This script is responsible for the appearance and scaling of
                 the DeveloperAssistant app.
'''

import os
import json
from typing import Optional, Dict
import customtkinter as ctk
from utils_dev_assist.dev_assist_logging import app_log

logger = app_log(__name__)


def get_appearance_mode(
        change_setting: bool = True) -> ctk.set_appearance_mode:
    '''
    This function retrieves and sets appearance mode based from
    the configuration file.
    '''

    gui_settings = read_config_file()

    if not change_setting:
        return gui_settings["theme"]

    logger.debug(" [SETTINGS] appearance mode -> set.")

    return ctk.set_appearance_mode(gui_settings["theme"])


def get_color_theme() -> ctk.set_default_color_theme:
    '''
    Responsible for retrieving the default color theme for the GUI elements
    of the application specified in the 'dev_assist_theme.json' file.
    '''

    logger.debug(" [SETTINGS] color theme -> set.")

    return ctk.set_default_color_theme("assets/dev_assist_theme.json")


def change_appearance_mode(new_mode: str) -> ctk.set_appearance_mode:
    '''
    Changes the GUI appearance and stores the mode chosen in the config file.
    '''

    scale = get_scale(change_setting=False)
    write_config_file(theme=new_mode, scale=scale)

    logger.debug(" [SETTINGS] appearance has been changed.")

    return ctk.set_appearance_mode(new_mode)


def get_scale(change_setting: bool = True) -> ctk.set_widget_scaling:
    '''
    Returns the scale of the GUI from the config file.
    '''

    gui_settings = read_config_file()

    if not change_setting:
        return gui_settings["scale"]

    logger.debug(" [SETTINGS] scaling -> set.")

    return ctk.set_widget_scaling(gui_settings["scale"])


def change_scaling(new_scaling: str) -> ctk.set_widget_scaling:
    '''
    Changes the scale of the GUI.
    '''

    new_scaling_setting = int(new_scaling.replace("%", "")) / 100

    theme = get_appearance_mode(change_setting=False)
    write_config_file(theme=theme, scale=new_scaling)

    logger.debug(" [SETTINGS] app scale changed.")

    return ctk.set_widget_scaling(new_scaling_setting)


def write_config_file(theme: Optional[str] = None,
                      scale: Optional[str] = None) -> None:
    '''
    Writes a JSON config file for the 'theme' of the appearance mode and
    'scale' for the GUI scaling.
    '''

    if theme is None:
        theme = "System"

    if scale is None:
        scale = "100"

    with open(".gui_config.cfg", "w", encoding="utf-8") as cfg:
        gui_settings = {"theme": theme,
                        "scale": scale}

        cfg.write(json.dumps(gui_settings, indent=4))

        logger.debug(" [SETTINGS] config file -> created!")


def read_config_file() -> Dict[str,str]:
    '''
    Retrieves settings from the config file.
    '''

    with open(".gui_config.cfg", "r", encoding="utf-8") as cfg:
        gui_settings = json.load(cfg)

        return gui_settings


CONFIG_FILE = ".gui_config.cfg"

if not os.path.isfile(CONFIG_FILE):
    write_config_file()
