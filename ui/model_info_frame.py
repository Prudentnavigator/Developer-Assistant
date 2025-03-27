#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
modelinfo_frame.py--Creates a frame to display information of the loaded model
                    for the Developer Assistant app.
'''

import customtkinter as ctk
from utils_dev_assist.dev_assist_logging import app_log
from utils_dev_assist import llm_models as lm

logger = app_log(__name__)


class ModelInfoFrame(ctk.CTkFrame):
    '''
    Class to create a frame for the DeveloperAssistant GUI with
    widgets for displaying the modelinfo.
    '''

    def __init__(self, DevAssistant, loaded_model):
        super().__init__(DevAssistant)
        self.loaded_model = loaded_model
        self.parent = DevAssistant
        self.modelinfo = ["modelfile",
                          "detail",
                          "parameter",
                          "template",
                          "system",
                          "adaptor",
                          "license"]

        self.widget = {"tabs": None,
                       "modelfile_text": None,
                       "details_text": None,
                       "parameters_text": None,
                       "template_text": None,
                       "system_text": None,
                       "adapter_text": None,
                       "license_text": None,
                       "back_button": None}

        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.grid_columnconfigure((1, 2, 3), weight=1)

        self.configure(corner_radius=30,
                       fg_color=("gray80", "gray15"),
                       border_width=3)

        self.modelinfo_frame_widgets()

    def modelinfo_frame_widgets(self) -> None:
        """
        Creates the GUI elements for the modelinfo frame.
        """

        self.widget["tabs"] = ctk.CTkTabview(self,
                                             bg_color="transparent",
                                             corner_radius=30)

        for info in self.modelinfo:
            self.widget["tabs"].add(info)
            args = self.widget["tabs"].tab(info)
            self.widget[f"{info}_text"] = ctk.CTkTextbox(args)

        green = ("#236538", "#067f2c")
        self.widget["back_button"] = ctk.CTkButton(
                                                self,
                                                text="go back",
                                                fg_color="transparent",
                                                border_width=2,
                                                border_color=green,
                                                text_color=("gray10",
                                                            "#DCE4EE"),
                                                command=self.destroy)

        logger.debug(" [GUI] create_model_gui_widgets -> created.")

        self.modelinfo_frame_layout()

    def modelinfo_frame_layout(self) -> None:
        """
        Creates the layout of the GUI elements for the modelinfo frame.
        """

        self.widget["tabs"].grid(row=0,
                                 rowspan=4,
                                 column=1,
                                 columnspan=3,
                                 padx=10,
                                 pady=10,
                                 sticky="nsew")

        for info in self.modelinfo:
            self.widget["tabs"].tab(info).grid_columnconfigure((0, 1, 2, 3),
                                                               weight=1)

            self.widget["tabs"].tab(info).grid_rowconfigure((0, 1, 2, 3),
                                                            weight=1)

            self.widget[f"{info}_text"].grid(row=0,
                                             column=0,
                                             rowspan=4,
                                             columnspan=4,
                                             sticky="nsew")

            self.widget[f"{info}_text"].configure(wrap="word")

            get_info = lm.show_model_info(self.loaded_model, info)

            self.widget[f"{info}_text"].insert("end", get_info)

        self.widget["back_button"].grid(row=5,
                                        column=2,
                                        pady=(10, 20),
                                        sticky="nsew")

        # Place frame into GUI.
        self.grid(row=0,
                  column=1,
                  rowspan=5,
                  padx=15,
                  pady=15,
                  sticky="nsew")
