#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
sidebar_frame.py--Creates a sidebar frame for the Developer Assistant app.
'''

import customtkinter as ctk
from utils_dev_assist.dev_assist_logging import app_log
from utils_dev_assist import gui_settings
logger = app_log(__name__)

# Get initial appearance.
gui_settings.get_appearance_mode()

# Get the app color theme.
gui_settings.get_color_theme()


class SideBarFrame(ctk.CTkFrame):
    '''
    Class to create a sidebar frame with widgets within the
    DeveloperAssistant GUI.
    '''

    def __init__(self, DevAssistant):
        super().__init__(DevAssistant)
        self.parent = DevAssistant
        self.widget = {"model_menu": None,
                       "info_button": None,
                       "download_button": None,
                       "create_button": None,
                       "delete_button": None,
                       "appearance_label": None,
                       "appearance_menu": None,
                       "scaling_label": None,
                       "scaling_menu": None,
                       "copyright_label": None}

        # Place the sidebar frame in the GUI layout.
        self.grid(row=0,
                  column=0,
                  rowspan=11,
                  sticky="nsew")

        self.grid_rowconfigure(5, weight=1)

        self.sidebar_frame_widgets()

    def sidebar_frame_widgets(self) -> None:
        '''
        Creates various widgets for the sidebar frame..

        Args:
            None

        Returns:
            none
        '''

        # optionmenu for loading a model used for a request.
        self.widget["model_menu"] = ctk.CTkOptionMenu(
                                              self,
                                              dynamic_resizing=False,
                                              values=self.parent.llm["models"],
                                              command=self.parent.load_llm)
        cmd = self.parent.load_modelinfo_frame
        self.widget["info_button"] = ctk.CTkButton(self,
                                                   text="model info",
                                                   command=cmd)

        # button for downloading llm's which opens a dialog window.
        cmd = self.parent.popup_dialog
        self.widget["download_button"] = ctk.CTkButton(
                                                  self,
                                                  text="download model",
                                                  command=cmd)

        # button for creating a model.
        self.widget["create_button"] = ctk.CTkButton(
                                                    self,
                                                    text="create model",
                                                    command=self.create_llm)

        # button for deleting a model.
        self.widget["delete_button"] = ctk.CTkButton(
                                                    self,
                                                    text="delete model",
                                                    command=self.delete_llm)

        # appearance mode and scaling options widgets.
        self.widget["appearance_label"] = ctk.CTkLabel(
                                                    self,
                                                    text="appearance mode:",
                                                    anchor="w")

        options = ["System", "Dark", "Light"]
        cmd = gui_settings.change_appearance_mode
        self.widget["appearance_menu"] = ctk.CTkOptionMenu(
                                                self,
                                                values=options,
                                                command=cmd)

        self.widget["scaling_label"] = ctk.CTkLabel(
                                                    self,
                                                    text="ui scaling:",
                                                    anchor="w")

        settings = ["80%", "90%", "100%", "110%", "120%"]
        cmd = gui_settings.change_scaling
        self.widget["scaling_menu"] = ctk.CTkOptionMenu(
                                                    self,
                                                    values=settings,
                                                    command=cmd)

        # copyright label widget.
        cpr = "copyright\xa92025 \n Thomas Pirchmoser"
        self.widget["copyright_label"] = ctk.CTkLabel(
                                                    self,
                                                    text=cpr,
                                                    font=("", 10))

        logger.debug(" [gui] main widgets -> created.")

        self.sidebar_frame_widgets_layout()

    def sidebar_frame_widgets_layout(self) -> None:
        '''
        this method is responsible for creating the layout of a gui interface.
        it places various widgets on the screen in a specific order and with
        certain padding and spacing.

        args:
            startup (bool): Is true on startup and false when widgets are
                            re-created.

        Returns:
            None
        '''

        self.widget["model_menu"].grid(row=0,
                                       column=0,
                                       padx=10,
                                       pady=(40, 0))

        # Set the initial value of the menu.
        self.widget["model_menu"].set("Load model")

        self.widget["info_button"].grid(row=1,
                                        column=0,
                                        padx=10,
                                        pady=(40, 10))

        self.widget["download_button"].grid(row=2,
                                            column=0,
                                            padx=10,
                                            pady=(10, 10))

        self.widget["create_button"].grid(row=3,
                                          column=0,
                                          padx=10,
                                          pady=(10, 10))

        self.widget["delete_button"].grid(row=4,
                                          column=0,
                                          padx=10,
                                          pady=(10, 65))

        self.widget["appearance_label"].grid(row=7,
                                             column=0,
                                             padx=10,
                                             pady=(10, 0))

        self.widget["appearance_menu"].grid(row=8,
                                            column=0,
                                            padx=10,
                                            pady=(5, 10))

        mode = gui_settings.get_appearance_mode(menu=True)

        self.widget["appearance_menu"].set(mode)

        self.widget["scaling_label"].grid(row=9,
                                          column=0,
                                          padx=10,
                                          pady=(10, 0))

        self.widget["scaling_menu"].grid(row=10,
                                         column=0,
                                         padx=10,
                                         pady=(5, 20))

        # Set initial value of the scale.
        self.widget["scaling_menu"].set(value="100%")

        self.widget["copyright_label"].grid(row=11,
                                            column=0,
                                            padx=(5, 5),
                                            pady=(5, 5))

        # Place frame to GUI.
        self.grid(row=0,
                  column=0,
                  rowspan=11,
                  padx=0,
                  pady=0,
                  sticky="nsew")

        logger.debug(" [GUI] main widgets layout -> completed.")

    def create_llm(self) -> None:
        '''
        Starts the proccess for the user to create a model.

        Args:
            None

        Returns:
            None:
        '''

        self.parent.load_create_model_frame()

    def delete_llm(self) -> None:
        '''
        Deletes the loaded model.

        Args:
            None

        Returns:
            None
        '''

        self.parent.delete_model()
        self.widget["model_menu"].configure(values=self.parent.llm["models"])

        # Reset the initial value of the menu.
        self.widget["model_menu"].set("Load model")
