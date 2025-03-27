#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
main_frame.py--Creates the main frame for interacting with a LLM for the
               Developer Assistant app.
'''

from time import sleep
import threading
from PIL import Image
from customtkinter import filedialog
import customtkinter as ctk
from utils_dev_assist.dev_assist_logging import app_log
from utils_dev_assist import dev_assist

logger = app_log(__name__)


class MainFrame(ctk.CTkFrame):
    '''
    Class to create the main frame for the DeveloperAssistant GUI with
    widgets for interacting with a model.
    '''

    def __init__(self, DevAssistant):
        super().__init__(DevAssistant)
        self.parent = DevAssistant
        self.request: str = ""
        self.attach_file: str = ""
        self.ai_response: str = ""

        self.widget = {"welcome_label": None,
                       "download_button": None,
                       "model_menu": None,
                       "info_menu": None,
                       "create_button": None,
                       "delete_button": None,
                       "appearance_label": None,
                       "appearance_menu": None,
                       "scaling_label": None,
                       "scaling_menu": None,
                       "copyright_label": None,
                       "request_text": None,
                       "submit_button": None,
                       "addfile_button": None,
                       "ai_response_textbox": None,
                       "progressbar": None}

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)

        self.configure(corner_radius=30,
                       fg_color=("gray80", "gray20"),
                       border_width=3)

        self.main_frame_widgets()

    def main_frame_widgets(self) -> None:
        '''
        Creates widgets for the main frame for interacting
        with a model.
        '''

        # entry widget for user input requests.
        plch_text = "How can I assist you?"
        self.widget["request_text"] = ctk.CTkEntry(self,
                                                   placeholder_text=plch_text,
                                                   font=("", 20),
                                                   height=45)

        # button to submit the request.
        green = ("#236538", "#067f2c")
        self.widget["submit_button"] = ctk.CTkButton(self,
                                                     fg_color="transparent",
                                                     border_width=2,
                                                     border_color=green,
                                                     text="submit",
                                                     text_color=("gray10",
                                                                 "#dce4ee"),
                                                     command=self.submit)

        # button to add a file to the request.
        self.widget["addfile_button"] = ctk.CTkButton(self,
                                                      fg_color="transparent",
                                                      border_width=2,
                                                      border_color=green,
                                                      text="attach file",
                                                      text_color=("gray10",
                                                                  "#dce4ee"),
                                                      command=self.select_file)

        # textbox to display ai_request, responses, info and error messages.
        self.widget["ai_response_textbox"] = ctk.CTkTextbox(self,
                                                            width=250,
                                                            font=("", 20),
                                                            corner_radius=40)

        # image to be used for the welcome label.
        img_path = "assets/welcome_screen.jpg"
        welc_image = ctk.CTkImage(light_image=Image.open(img_path),
                                  size=(1600, 840))

        # label for displaying a welcome image on app startup.
        # it will be removed from the layout when the first request
        # is submitted.
        welcome_text = "-->  Developer Assistant  <--"
        self.widget["welcome_label"] = ctk.CTkLabel(self,
                                                    image=welc_image,
                                                    text=welcome_text,
                                                    text_color="white",
                                                    font=("", 50),
                                                    corner_radius=40)

        logger.debug(" [gui] main widgets -> created.")

        self.main_frame_widgets_layout()

    def main_frame_widgets_layout(self) -> None:
        '''
        Creates the layout for the widgets of the main frame in order to
        interact with a model.
        '''

        self.widget["request_text"].grid(row=4,
                                         column=1,
                                         padx=(20, 0),
                                         pady=(10, 20),
                                         sticky="nsew")

        self.widget["submit_button"].grid(row=4,
                                          column=2,
                                          padx=(20, 20),
                                          pady=(20, 30),
                                          sticky="w")

        self.widget["addfile_button"].grid(row=4,
                                           column=3,
                                           padx=(20, 20),
                                           pady=(20, 30),
                                           sticky="e")

        # Label will be removed from the layout when the first request
        # is submitted.
        self.widget["welcome_label"].grid(row=0,
                                          rowspan=3,
                                          column=1,
                                          columnspan=3,
                                          padx=(20, 20),
                                          pady=(20, 20),
                                          sticky="nsew")

        self.grid(row=0,
                  column=1,
                  rowspan=5,
                  padx=15,
                  pady=15,
                  sticky="nsew")

        logger.debug(" [GUI] main widgets layout -> completed.")

    def check_welcome_label_widget(self) -> None:
        '''
        Checks if the welcome label widget is displayed and if so, remove it.

        Args:
          None

        Returns:
            None
        '''

        if self.widget["welcome_label"]:
            self.widget["welcome_label"].destroy()
            self.widget["welcome_label"] = None

            logger.debug(" [GUI] welcome label -> removed.")

            self.add_textbox_widget()

    def add_textbox_widget(self) -> None:
        '''
        Adds the reply text box widget to the GUI layout.
        '''

        self.widget["ai_response_textbox"].grid(row=0,
                                                rowspan=4,
                                                column=1,
                                                columnspan=3,
                                                padx=(20, 20),
                                                pady=(20, 20),
                                                sticky="nsew")

        logger.debug(" [GUI] textbox widget added to the layout.")

    def select_file(self) -> None:
        """
        Opens a file dialog to allow the user to select a file to attach to
        the request. If no file is selected, sets `self.attach_file` to an
        empty string.

        Args:
            None

        Returns:
            None
        """

        # Store the chosen file including its path.
        self.attach_file = filedialog.askopenfilename()

        if not self.attach_file:
            self.attach_file = ""
            logger.debug(" [ATTACH FILE] file attachment canceled!")

        else:
            logger.debug(" [ATTACH FILE] file %s attached to the request.",
                         self.attach_file)

    def submit(self) -> None:
        """
        Submits the current request and verifies that a model has been loaded.
        If no model is selected, a reminder message box will be displayed
        asking the user to load a model, otherwise the start_progressbar
        method is called.
        """

        if self.parent.check_model_loaded():
            self.check_welcome_label_widget()
            self.add_progressbar_widget()

    def add_progressbar_widget(self) -> None:
        '''
        Adds an indeterminate progress bar in the GUI and calls
        the start_thread method.
        '''

        self.widget["progressbar"] = ctk.CTkProgressBar(self,
                                                        mode="indeterminate")

        self.widget["progressbar"].grid(row=3,
                                        column=1,
                                        columnspan=3,
                                        padx=(200, 250),
                                        pady=(250, 0),
                                        sticky="ew")

        logger.debug(" [GUI] progress bar added to the layout.")

        self.start_thread()

    def progressbar(self, start: bool = True) -> None:
        '''
        Starts or stops and removes the progressbar from the GUI.
        '''

        if start:
            self.widget["progressbar"].start()
            logger.info(" progress bar --> started.")

        else:
            self.widget["progressbar"].stop()
            self.widget["progressbar"].destroy()

            logger.info(" [GUI] progress bar --> stopped.")

            logger.debug(" [GUI] progress bar removed from layout.")

    def start_thread(self) -> None:
        """
        Starts new threads to handle ai_requests.
        """

        request_thread = threading.Thread(target=self.ai_request,
                                          daemon=True)

        request_thread.start()
        logger.info(" [THREAD] request thread --> started.")

        self.progressbar(start=True)

    def ai_request(self) -> None:
        """
        Handles the request process.
        """

        self.widget["submit_button"].configure(state="disabled")
        self.widget["addfile_button"].configure(state="disabled")

        self.request = self.widget["request_text"].get()

        msg = f"\u27BE Your request: {self.request}\n"
        self.widget["ai_response_textbox"].insert("end", msg)

        if self.attach_file != "":
            msg = f"attached file: {self.attach_file}\n"
            self.widget["ai_response_textbox"].insert("end", msg)

        self.widget["ai_response_textbox"].yview_moveto(1.0)
        self.widget["ai_response_textbox"].configure(require_redraw=True)

        self.widget["request_text"].delete(0, "end")

        self.ai_response = dev_assist.ask(self.request,
                                          self.parent.llm["model"],
                                          self.attach_file)

        if self.ai_response.startswith("error"):
            self.parent.popup_message("response_error", self.ai_response)

            self.progressbar(start=False)
            self.attach_file = ""

        else:
            self.widget["ai_response_textbox"].configure(wrap="word")

            self.progressbar(start=False)
            self.copy_to_clipboard()
            self.display_response()

        self.widget["submit_button"].configure(state="normal")
        self.widget["addfile_button"].configure(state="normal")

    def display_response(self, response="") -> None:
        """
        Displays the response in the reply textbox widget, character by
        character, with a slight delay between each character to
        simulate typing.
        """

        if response != "":
            self.ai_response = response

        for char in self.ai_response:
            self.widget["ai_response_textbox"].insert("end", char)
            self.widget["ai_response_textbox"].yview_moveto(1.0)
            self.widget["ai_response_textbox"].configure(require_redraw=True)

            sleep(0.04)

        logger.info(" [GUI] response --> displayed.")

        self.attach_file = ""

    def copy_to_clipboard(self) -> None:
        '''
        Copies the last response automatically to the clipboard.
        '''

        self.clipboard_clear()
        self.clipboard_append(self.ai_response)
        logger.info(" response copied to --> clipboard.")
