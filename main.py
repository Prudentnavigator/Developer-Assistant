#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
Developer Assistant -- this application provides a GUI to interact with
                       locally installed LLM's (large language models) with
                       the use of Ollama ai.
                       It allows users to submit requests, receive responses,
                       attach files to their requests, download and delete
                       models, view model info, and create models.
                       The application uses customtkinter for its design and
                       supports multiple appearance modes and scaling options.
'''

import threading
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from ui.main_frame import MainFrame
from ui.sidebar_frame import SideBarFrame
from ui.model_info_frame import ModelInfoFrame
from ui.create_model_frame import CreateModelFrame
from utils_dev_assist import llm_models as lm
from utils_dev_assist.dev_assist_logging import app_log

logger = app_log(__name__)


class DevAssistant(ctk.CTk):
    '''
    Allows users to interact with a language model, submit requests,
    receive responses, view modelinfo and create models via a GUI.
    '''

    llm = {"model": "", "models": "", "new_model": ""}

    def __init__(self):
        super().__init__()

        # Configure main window.
        self.title("Developer Assistant v1.11.17")
        self.geometry(f"{1100}x{580}")

        # Configure grid layout (4x4).
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)

        # Create sidebar frame.
        self.sidebar_frame = ctk.CTkFrame(self)

        # Create main frame.
        self.main_frame = ctk.CTkFrame(self)

        self.load_sidebar_frame()
        MainFrame(self)

    def load_sidebar_frame(self) -> None:
        '''
        Loads the sidebar frame into to app.
        '''

        try:
            self.llm["models"] = lm.installed_models()

        except ConnectionError as error:
            self.popup_message(caller="server_connection",
                               msg=error,
                               icon="warning")

        SideBarFrame(self)

    def load_create_model_frame(self) -> None:
        '''
        Loads create model frame into the GUI main frame.
        '''

        if self.check_model_loaded():
            CreateModelFrame(self, self.llm["model"])

    def load_modelinfo_frame(self) -> None:
        '''
        Loads model info frame into the GUI main frame.
        '''

        if self.check_model_loaded():
            ModelInfoFrame(self, self.llm["model"])

    def load_llm(self, model: str) -> None:
        """
        Sets the language model for the instance.
        """

        self.llm["model"] = model

        logger.debug(" [LLM] %s has been selected.", self.llm["model"])

    def check_model_loaded(self) -> bool:
        '''
        Checks if a model is loaded.
        '''

        # If no model was loaded display a popup message.
        if self.llm["model"] == "":
            self.popup_message("check_model_loaded")

            return False

        return True

    def popup_dialog(self, caller: str = None) -> None | str:
        """
        This method is used to display a dialog box based on the
        given `caller`.
        """

        if caller is None:
            dialog = ctk.CTkInputDialog(title="Download LLM",
                                        text="enter a model:")

            logger.debug(" [GUI] download dialog -> displayed.")

            self.llm["new_model"] = dialog.get_input()

            if self.llm["new_model"] is None:
                return None

            msg = f"Starting download of {self.llm['new_model']}..."
            self.popup_message("download_start", msg)

            # Call the start_thread method.
            self.start_thread()

        if caller == "create_model":
            # Dialog popup to request the name for the model to create.
            msg = "Please enter the name of the new model."
            new_model_name = ctk.CTkInputDialog(title="Create Model",
                                                text=msg)

            logger.debug(" [GUI] create model dialog -> displayed.")

            model_name = new_model_name.get_input()

            return model_name

    def popup_message(self, caller: str,
                      msg: str = "",
                      icon: str = "info") -> None | str:
        """
        This method is used to display a message box based on the
        given `caller`.
        """

        if caller == "server_connection":
            CTkMessagebox(title="Ollama Server",
                          message=msg,
                          icon=icon,
                          option_1="ok",
                          justify="center",
                          fade_in_duration=2)

            logger.debug(" [GUI] load model reminder msg -> displayed.")

        if caller == "check_model_loaded":
            CTkMessagebox(title="Reminder",
                          message="Please load a model!",
                          icon=icon,
                          option_1="ok",
                          justify="center",
                          fade_in_duration=2)

            logger.debug(" [GUI] load model reminder msg -> displayed.")

        elif caller == "delete_model":
            if icon == "info":
                deleted = CTkMessagebox(title="Delete model",
                                        message=msg,
                                        icon=icon,
                                        option_1="ok",
                                        justify="center",
                                        fade_in_duration=2)

                # Close popup message automatically.
                deleted.after(2000, deleted.destroy)

            else:
                confirmation = CTkMessagebox(message=msg,
                                             title="Warning!",
                                             title_color="red",
                                             corner_radius=15,
                                             font=("", 20),
                                             icon=icon,
                                             option_1="cancel",
                                             option_2="yes",
                                             justify="center",
                                             fade_in_duration=2)

                msg = " [GUI] delete model confirmation msg -> displayed."
                logger.debug(msg)

                return confirmation

        elif caller == "create_model":
            created = CTkMessagebox(title="Created Model",
                                    message=msg,
                                    icon="info",
                                    option_1="ok",
                                    justify="center",
                                    fade_in_duration=2)

            created.after(2000, created.destroy)

        elif caller == "download":
            CTkMessagebox(title="Download Model",
                          message=msg,
                          icon=icon,
                          option_1="ok",
                          justify="left",
                          fade_in_duration=2)

        elif caller == "download_start":
            popup_msg = CTkMessagebox(title="Download Model",
                                      message=msg,
                                      icon=icon,
                                      option_1="ok",
                                      justify="center",
                                      fade_in_duration=2)

            popup_msg.after(2000, popup_msg.destroy)

        elif caller == "response_error":
            error_msg = CTkMessagebox(title="Load Model",
                                      message=msg,
                                      icon=icon,
                                      option_1="ok",
                                      justify="center",
                                      fade_in_duration=2)

            error_msg.after(5000, error_msg.destroy)

    def download_model(self) -> None:
        """
        Downloads and installs a new LLM model.
        """

        # Display download message in the tex box.
        model = self.llm['new_model']

        download_msg = lm.download_install_model(model)
        self.popup_message(caller="download", msg=download_msg)

        self.load_sidebar_frame()

    def delete_model(self) -> None:
        '''
        Deletes the model that was loaded by the user.
        '''

        if self.llm["model"] is None:
            self.submit()

        else:
            msg = f"Are you sure you want to delete {self.llm['model']}?"
            confirmation = self.popup_message("delete_model",
                                              msg, icon="warning")

            # Get the option loaded by the user.
            remove = confirmation.get()

            if remove == "yes":
                deleted = lm.delete_model(self.llm["model"])
                if deleted:
                    msg = f"{self.llm['model']} deleted!"
                    self.popup_message("delete_model", msg)

                # Retrieve the updated list of models.
                self.llm["models"] = lm.installed_models()

    def start_thread(self) -> None:
        """
        Starts new threads to handle downloads.
        """

        # Create and start a new deamon thread for downloading a LLM.
        download_thread = threading.Thread(target=self.download_model)
        download_thread.start()
        logger.info(" [THREAD] download thread --> started.")


# Entry point of the application.
if __name__ == "__main__":
    logger.info("[START] application is starting...")

    app = DevAssistant()
    app.mainloop()

    logger.info("[STOPT] application closed by the user.")
