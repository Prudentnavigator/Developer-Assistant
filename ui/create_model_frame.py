#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
create_model_frame.py -- Creates a frame that contains the widgets
                         and their layout for creating a new model.
'''

import customtkinter as ctk
from utils_dev_assist.dev_assist_logging import app_log
from utils_dev_assist import llm_models as lm

logger = app_log(__name__)


class CreateModelFrame(ctk.CTkFrame):
    '''
    Class to create a frame for the DeveloperAssistant GUI with
    widgets for creating a LLM.
    '''

    def __init__(self, DevAssistant, base_model):
        super().__init__(DevAssistant)
        self.base_model = base_model
        self.parent = DevAssistant
        self.widget = {"tabs": None,
                       "modfile_text": None,
                       "help_text": None,
                       "create_button": None,
                       "cancel_button": None}

        # Set the row and column configuration.
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.grid_columnconfigure((1, 2, 3), weight=1)

        # Set frame attributes.
        self.configure(corner_radius=30,
                       fg_color=("gray80", "gray15"),
                       border_width=3)

        self.create_model_frame_widgets()

    def create_model_frame_widgets(self) -> None:
        """
        This method creates the GUI elements to create a new model and
        canceling this process.
        """

        # Create tabviews.
        self.widget["tabs"] = ctk.CTkTabview(self,
                                             bg_color="transparent",
                                             corner_radius=30)

        self.widget["tabs"].add("edit modelfile")
        self.widget["tabs"].add("help")

        # Text box widget for displaying a modelfile of the loaded model.
        args = self.widget["tabs"].tab("edit modelfile")
        self.widget["modfile_text"] = ctk.CTkTextbox(args)

        # Text box widget for displaying a modelfile help text.
        args = self.widget["tabs"].tab("help")
        self.widget["help_text"] = ctk.CTkTextbox(args)

        # Create a 'create_cancel_button' widget.
        green = ("#236538", "#067f2c")
        cmd = self.cancel_create_model
        self.widget["cancel_button"] = ctk.CTkButton(
                                                self,
                                                text="cancel",
                                                fg_color="transparent",
                                                border_width=2,
                                                border_color=green,
                                                text_color=("gray10",
                                                            "#DCE4EE"),
                                                command=cmd)

        # Create and add to the layout a 'create_model_button' widget.
        self.widget["create_button"] = ctk.CTkButton(
                                                self,
                                                text="save modelfile",
                                                fg_color="transparent",
                                                border_width=2,
                                                border_color=green,
                                                text_color=("gray10",
                                                            "#DCE4EE"),
                                                command=self.create_new_model)

        logger.debug(" [GUI] create_model_gui_widgets -> created.")

        self.create_model_frame_layout()

    def create_model_frame_layout(self) -> None:
        """
        This method is responsible for creating the layout of the
        GUI elements.
        """

        self.widget["tabs"].grid(row=0,
                                 rowspan=4,
                                 column=1,
                                 columnspan=3,
                                 padx=10,
                                 pady=10,
                                 sticky="nsew")

        self.widget["tabs"].tab("edit modelfile").grid_columnconfigure(
                                                                  (0, 1, 2, 3),
                                                                  weight=1)

        self.widget["tabs"].tab("edit modelfile").grid_rowconfigure(
                                                                (0, 1, 2, 3),
                                                                weight=1)

        self.widget["tabs"].tab("help").grid_columnconfigure((0, 1, 2, 3),
                                                             weight=1)

        self.widget["tabs"].tab("help").grid_rowconfigure((0, 1, 2, 3),
                                                          weight=1)

        self.widget["modfile_text"].grid(row=0,
                                         column=0,
                                         rowspan=4,
                                         columnspan=4,
                                         sticky="nsew")

        self.widget["modfile_text"].configure(wrap="word")

        # Get modelfile of the base model for the model to create.
        modelfile = lm.show_model_info(self.base_model, "modelfile")

        self.widget["modfile_text"].insert("end", modelfile)

        self.widget["help_text"].grid(row=0,
                                      column=0,
                                      rowspan=4,
                                      columnspan=4,
                                      sticky="nsew")

        self.widget["cancel_button"].grid(row=4,
                                          column=1,
                                          padx=(80, 10),
                                          pady=(10, 20),
                                          sticky="nsew")

        self.widget["create_button"].grid(row=4,
                                          column=3,
                                          padx=(10, 80),
                                          pady=(10, 20),
                                          sticky="nsew")

        logger.debug(" [GUI] create_model_widgets layout  -> completed.")

        # Place frame into GUI.
        self.grid(row=0, column=1, rowspan=5, padx=15, pady=15, sticky="nsew")

        # Display a modelfile help text in the 'help_text' widget.
        self.widget["help_text"].insert("end", lm.help_create_model())

    def create_new_model(self) -> None:
        '''
        Creates a new model by using a popup dialog from the parent class
        to request the user for a name of the model and passes the name and
        modelfile to the 'lm_create_model()'.
        '''

        # Request the user to provide a name for the new model.
        new_model_name = self.parent.popup_dialog("create_model")

        # If the popup got canceled quit the method.
        if new_model_name is None:
            return

        # Retrieve the edited modelfile from the modelfile text widget.
        modelfile = self.widget["modfile_text"].get("0.0", "end")

        # Pass the name and modelfile of the new model to the
        # 'lm.create_model()'.
        lm.create_model(new_model_name, modelfile)

        # Display that the model was created in the modelfile text widget.
        msg = f"Model {new_model_name} created!"
        self.parent.popup_message("create_model", msg)

        logger.info("Model %s created!", new_model_name)
        self.parent.load_sidebar_frame()

        self.destroy()

    def cancel_create_model(self) -> None:
        """
        Cancels the creation of a model and destroys the frame
        of the create model functionality.
        """

        logger.debug(" create model -> canceled.")

        self.destroy()
