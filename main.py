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
                       models, and view model details.
                       The application uses customtkinter for its design and
                       supports multiple appearance modes and scaling options.
'''

from time import sleep
import threading
import customtkinter as ctk
from PIL import Image
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
from utils_dev_assist import llm_models
from utils_dev_assist import dev_assist
from utils_dev_assist.dev_assist_logging import app_log

logger = app_log(__name__)

# Set initial appearance ("System", "Light", "Dark")
ctk.set_appearance_mode("System")

# Assign the app color theme from the .json file, which can be modified
# according to taste.
ctk.set_default_color_theme("assets/dev_assist_theme.json")


class DevAssistant(ctk.CTk):
    '''
    Allows users to interact with a language model,
    submit requests, and receive responses via a GUI.
    '''

    def __init__(self):
        super().__init__()
        self.request = ""
        self.attach_file = ""
        self.response = ""
        self.llm = {"model": None,
                    "models": llm_models.installed_models(),
                    "new_model": None}

        self.widget = {"welcome_label": None,
                       "download_button": None,
                       "model_menu": None,
                       "detail_button": None,
                       "delete_button": None,
                       "appearance_label": None,
                       "appearance_menu": None,
                       "scaling_label": None,
                       "scaling_menu": None,
                       "copyright_label": None,
                       "entry_text": None,
                       "entry_button": None,
                       "addfile_button": None,
                       "reply_textbox": None,
                       "progressbar": None}

        # Configure window.
        self.title("Developer Assistant v1.0.0")
        self.geometry(f"{1100}x{580}")

        # Configure grid layout (4x4).
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame.
        self.sidebar_frame = ctk.CTkFrame(self,
                                          width=140,
                                          corner_radius=5)

        # Place the sidebar frame in the GUI layout.
        self.sidebar_frame.grid(row=0,
                                column=0,
                                rowspan=5,
                                sticky="nsew")

        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.create_widgets()

    def create_widgets(self) -> None:
        '''
        This method creates various widgets for a GUI interface.
        It is responsible for creating an option menu to load a Language Model
        (LLM) used for a request, as well as buttons for downloading LLM's,
        showing details about the loaded LLM, deleting a LLM, and changing the
        appearance mode and scaling options of the interface.
        Additionally, it creates a copyright label, a welcome label, an entry
        widget for user input, a button to submit the request, a button to
        attach a file to the request. A textbox to display requests and
        responses will be created upon the first request.
        Popup messages and progress bar will be created as and when needed.

        Args:
            None

        Returns:
            None
        '''

        # Optionmenu for loading a model used for a request.
        self.widget["model_menu"] = ctk.CTkOptionMenu(
                                                    self.sidebar_frame,
                                                    dynamic_resizing=False,
                                                    values=self.llm["models"],
                                                    command=self.load_llm)

        # Button for downloading LLM's which opens a dialog window.
        self.widget["download_button"] = ctk.CTkButton(
                                                  self.sidebar_frame,
                                                  text="Download LLM",
                                                  command=self.download_dialog)

        # Button for showing details about the loaded model.
        self.widget["detail_button"] = ctk.CTkButton(
                                                    self.sidebar_frame,
                                                    text="Details of LLM",
                                                    command=self.model_detail)

        # Button for deleting a model.
        self.widget["delete_button"] = ctk.CTkButton(
                                                    self.sidebar_frame,
                                                    text="Delete LLM",
                                                    command=self.delete_model)

        # Appearance mode and scaling options widgets.
        self.widget["appearance_label"] = ctk.CTkLabel(
                                                    self.sidebar_frame,
                                                    text="Appearance Mode:",
                                                    anchor="w")

        options = ["System", "Dark", "Light"]
        self.widget["appearance_menu"] = ctk.CTkOptionMenu(
                                                self.sidebar_frame,
                                                values=options,
                                                command=change_appearance_mode)

        self.widget["scaling_label"] = ctk.CTkLabel(
                                                    self.sidebar_frame,
                                                    text="UI Scaling:",
                                                    anchor="w")

        settings = ["80%", "90%", "100%", "110%", "120%"]
        self.widget["scaling_menu"] = ctk.CTkOptionMenu(
                                                    self.sidebar_frame,
                                                    values=settings,
                                                    command=change_scaling)

        # Copyright label widget.
        cpr = "Copyright\xa92025 \n Thomas Pirchmoser"
        self.widget["copyright_label"] = ctk.CTkLabel(
                                                    self.sidebar_frame,
                                                    text=cpr,
                                                    font=("", 10))

        # Entry widget for user input requests.
        plch_text = "How can i assist you?"
        self.widget["entry_text"] = ctk.CTkEntry(
                                                self,
                                                placeholder_text=plch_text,
                                                font=("", 20),
                                                height=45,
                                                corner_radius=15)

        # Button to submit the request.
        green = ("#236538", "#067f2c")
        self.widget["entry_button"] = ctk.CTkButton(
                                                    self,
                                                    fg_color="transparent",
                                                    border_width=2,
                                                    border_color=green,
                                                    text="Submit",
                                                    text_color=("gray10",
                                                                "#DCE4EE"),
                                                    command=self.submit)

        # Button to add a file to the request.
        self.widget["addfile_button"] = ctk.CTkButton(
                                                    self,
                                                    fg_color="transparent",
                                                    border_width=2,
                                                    border_color=green,
                                                    text="Attach file",
                                                    text_color=("gray10",
                                                                "#DCE4EE"),
                                                    command=self.select_file)

        # Textbox to display requests, responses, info and error messages.
        self.widget["reply_textbox"] = ctk.CTkTextbox(
                                                      self,
                                                      width=250,
                                                      font=("", 20),
                                                      corner_radius=15)

        # Image to be used for the welcome label.
        img_path = "assets/welcome_screen.jpg"
        welc_image = ctk.CTkImage(light_image=Image.open(img_path),
                                  size=(1600, 840))

        # Label for displaying a welcome image on app startup.
        # It will be removed from the layout when the first request
        # is submitted.
        welcome_text = "-->  Developer Assistant  <--"
        self.widget["welcome_label"] = ctk.CTkLabel(self, image=welc_image,
                                                    text=welcome_text,
                                                    text_color="white",
                                                    font=("", 50))

        logger.debug(" [GUI] main widgets created.")

        self.widgets_gui_layout()

    def widgets_gui_layout(self) -> None:
        '''
        This method is responsible for creating the layout of a GUI interface.
        It places various widgets on the screen in a specific order and with
        certain padding and spacing.

        Args:
            None

        Returns:
            None
        '''

        self.widget["model_menu"].grid(row=0,
                                       column=0,
                                       padx=10,
                                       pady=(40, 0))

        # Set the initial value of the menu.
        self.widget["model_menu"].set("Load model")

        self.widget["download_button"].grid(row=2,
                                            column=0,
                                            padx=10,
                                            pady=(100, 5))

        self.widget["detail_button"].grid(row=3,
                                          column=0,
                                          padx=10,
                                          pady=(15, 5))

        self.widget["delete_button"].grid(row=4,
                                          column=0,
                                          padx=10,
                                          pady=(15, 40),
                                          sticky="n")

        self.widget["appearance_label"].grid(row=5,
                                             column=0,
                                             padx=10,
                                             pady=(10, 0))

        self.widget["appearance_menu"].grid(row=6,
                                            column=0,
                                            padx=10,
                                            pady=(10, 10))

        self.widget["scaling_label"].grid(row=7,
                                          column=0,
                                          padx=10,
                                          pady=(10, 0))

        self.widget["scaling_menu"].grid(row=8,
                                         column=0,
                                         padx=10,
                                         pady=(10, 20))

        # Set initial value of the scale.
        self.widget["scaling_menu"].set(value="100%")

        self.widget["copyright_label"].grid(row=9,
                                            column=0,
                                            padx=(5, 5),
                                            pady=(5, 5))

        self.widget["entry_text"].grid(row=4,
                                       column=1,
                                       padx=(20, 0),
                                       pady=(10, 20),
                                       sticky="nsew")

        self.widget["entry_button"].grid(row=4,
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
                                          padx=(10, 10),
                                          pady=(10, 10),
                                          sticky="nsew")

        logger.debug(" [GUI] main widgets layout completed.")

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
            logger.debug(" [GUI] welcome label removed.")

            self.add_textbox_widget()

    def add_textbox_widget(self) -> None:
        '''
        Adds the reply text box widget to the GUI layout.

        Args:
          None

        Returns:
            None
        '''

        self.widget["reply_textbox"].grid(row=0,
                                          rowspan=3,
                                          column=1,
                                          columnspan=3,
                                          padx=(40, 40),
                                          pady=(40, 40),
                                          sticky="nsew")

        logger.debug(" [GUI] textbox widget added to the layout.")

    def create_progressbar_widget(self) -> None:
        '''
        Creates an indeterminate progress bar in the GUI and calls
        the start_thread method.

        Args:
            None

        Returns:
            None
        '''

        # Progress bar to indicate to the user that the request is processing
        self.widget["progressbar"] = ctk.CTkProgressBar(self,
                                                        mode="indeterminate")

        self.widget["progressbar"].grid(row=3,
                                        column=1,
                                        columnspan=3,
                                        padx=(200, 250),
                                        pady=(0, 15),
                                        sticky="ew")

        logger.debug(" [GUI] progress bar created and added to the layout.")

        self.start_thread()

    def stop_progressbar(self) -> None:
        '''
        Stops and removes the progressbar from the GUI.

        Args:
            None

        Returns:
            None
        '''

        self.widget["progressbar"].stop()
        self.widget["progressbar"].destroy()

        logger.info(" [GUI] progress bar --> stopped.")

        logger.debug(" [GUI] progress bar removed from layout.")

    def load_llm(self, model: str) -> None:
        """
        Sets the language model for the instance.

        Args:
            model (object): The language model to be used.

        Returns:
            None
        """

        self.llm["model"] = model

        logger.debug(" [LLM] %s has been selected.", self.llm["model"])

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
            logger.debug(" no file attached to the request.")

        logger.debug(" file %s attached to the request.", self.attach_file)

    def submit(self) -> None:
        """
        Submits the current request and verifies that a model has been loaded.
        If no model is selected, a reminder message box will be displayed
        asking the user to load a model, otherwise the start_progressbar
        method is called.

        Args:
            None

        Returns:
            None
        """

        # If no model was loaded display a popup message.
        if self.llm["model"] is None:
            CTkMessagebox(title="Reminder",
                          message="Please load a model!",
                          icon="info",
                          option_1="ok")
        else:
            self.check_welcome_label_widget()
            self.create_progressbar_widget()

    def download_dialog(self) -> None:
        """
        Displays a dialog window that prompts the user to input the name of a
        LLM they wish to download and install. The entered model name is then
        stored in 'llm['new_model']'.

        Args:
            None

        Returns:
            None
        """

        # Create an input dialog window asking the user to enter a model name.
        dialog = ctk.CTkInputDialog(text="enter a model:",
                                    title="Download/Install LLM")

        # Retrieve the user's input from the dialog.
        self.llm["new_model"] = dialog.get_input()

        if self.llm["new_model"] is None:
            return

        # Call the start_thread method.
        self.start_thread(query=False)

    def download_install_model(self) -> None:
        """
        Downloads and installs a new LLM model.

        This method checks if the welcome label widget is visible, then
        downloads and installs a new LLM model using the llm_models module.
        It updates the response attribute with the status of the download
        process and displays it in the GUI.
        Afterwards, it retrieves the list of installed models and updates the
        model dropdown menu accordingly.

        Args:
            None

        Returns:
            None
        """

        self.check_welcome_label_widget()

        # Display download message in the tex box.
        model = self.llm['new_model']
        self.response = f"\n--> downloading {model}! <--\n"
        self.display_response()

        self.response = llm_models.download_install_model(model)

        self.display_response()

        # Retrieve the updated list of models.
        self.llm["models"] = llm_models.installed_models()

        # Add the new model to the 'model_menu'.
        self.widget["model_menu"].configure(values=self.llm["models"])

    def model_detail(self) -> None:
        '''
        Gets info about the loaded model.

        Args:
            None

        Returns:
            None
        '''

        if self.llm["model"] is not None:
            idx = self.llm["models"].index(self.llm["model"])
            self.response = llm_models.show_model_details(idx,
                                                          self.llm["model"])

            self.check_welcome_label_widget()

            # Display model info in the text box.
            self.display_response()

        else:
            CTkMessagebox(title="Reminder",
                          message="Please load a model!",
                          icon="info",
                          option_1="ok")

    def delete_model(self) -> None:
        '''
        Deletes the model that was loaded by the user.
        Displays a message box that asks for confirmation.

        Parmeters:
            None

        Returns:
            None
        '''

        if self.llm["model"] is None:
            self.submit()

        else:
            message = f"Are you sure you want to delete {self.llm['model']}?"
            confirmation = CTkMessagebox(message=message,
                                         title="Warning!",
                                         title_color="red",
                                         corner_radius=15,
                                         font=("", 20),
                                         icon="warning",
                                         option_1="cancel",
                                         option_2="yes")

            # Get the option loaded by the user.
            remove = confirmation.get()

            if remove == "yes":
                self.check_welcome_label_widget()
                self.response = llm_models.delete_model(self.llm["model"])
                self.display_response()

    def start_thread(self, query: bool = True) -> None:
        """
        Starts new threads to handle requests and/or downloads.

        Args:
            query (bool): A boolean value that determines whether to start the
                          request or download handling thread .
        Returns:
            None
        """

        if query:
            # Create and start a new daemon thread for handling requests.
            request_thread = threading.Thread(target=self.requests,
                                              daemon=True)
            request_thread.start()
            logger.info(" [THREAD] request thread --> started.")

            # Actitvate a progressbar while request is beeing processed
            self.widget["progressbar"].start()
            logger.info(" progress bar --> started.")

        else:
            download = self.download_install_model

            # Create and start a new deamon thread for downloading a LLM.
            download_thread = threading.Thread(target=download)
            download_thread.start()
            logger.info(" [THREAD] download thread --> started.")

    def requests(self) -> None:
        """
        Handles the request process by:

        1. Retrieving the text from an entry widget.
        2. Inserting the request into a textbox widget with a formatted string.
        3. Scrolling to the end of the textbox and configuring it for
           redrawing.
        4. Clearing the entry widget.
        5. Sending the request to a code assistance function.
        6. Configuring the textbox to wrap text by word.
        7. Stopping the progress bar.
        8. Copying the response to the clipboard.
        9. Calling the display_response method.

        Args:
            None

        Returns:
            None
        """

        self.request = self.widget["entry_text"].get()

        msg = f"\u27BE Your request: {self.request}\n"
        self.widget["reply_textbox"].insert("end", msg)

        if self.attach_file != "":
            msg = f"attached file: {self.attach_file}\n"
            self.widget["reply_textbox"].insert("end", msg)

        self.widget["reply_textbox"].yview_moveto(1.0)
        self.widget["reply_textbox"].configure(require_redraw=True)

        self.widget["entry_text"].delete(0, "end")

        self.response = dev_assist.ask(self.request,
                                       self.llm["model"],
                                       self.attach_file)

        self.widget["reply_textbox"].configure(wrap="word")

        self.stop_progressbar()
        self.copy_to_clipboard()
        self.display_response()

    def display_response(self) -> None:
        """
        Displays the response in the request textbox widget, character by
        character, with a slight delay between each character to
        simulate typing.
        This method iterates over each character in `self.response`,
        inserts it into the "reply_textbox" widget, and scrolls to the end
        of the text. It also ensures that the widget is redrawn after
        each insertion. After displaying all characters, it resets the
        `attach_file` attribute to an empty string.

        Args:
            None

        Returns:
            None
        """

        for char in self.response:
            self.widget["reply_textbox"].insert("end", char)
            self.widget["reply_textbox"].yview_moveto(1.0)
            self.widget["reply_textbox"].configure(require_redraw=True)

            sleep(0.04)

        logger.info(" [GUI] response --> displayed.")

        self.attach_file = ""

    def copy_to_clipboard(self) -> None:
        '''
        Copies the last response automatically to the clipboard.

        Args:
            None

        Returns:
            None
        '''

        app.clipboard_clear()
        app.clipboard_append(self.response)
        logger.info(" response copied to --> clipboard.")


def change_appearance_mode(new_appearance_mode: str) -> None:
    '''
    Changes GUI appearance.

    Args:
        str: new_appearance_mode (settings for a new appearance).

    Returns:
        None
    '''

    ctk.set_appearance_mode(new_appearance_mode)
    logger.debug(" [GUI] appearance has been changed.")


def change_scaling(new_scaling: str) -> None:
    '''
    Changes the scale of the GUI.

    Args:
        str: new_scaling

    Returns:
        None
    '''

    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    ctk.set_widget_scaling(new_scaling_float)
    logger.debug(" [GUI] app scale changed.")


# Entry point of the application.
if __name__ == "__main__":
    logger.info("[START] application is starting...")

    app = DevAssistant()
    app.mainloop()

    logger.info("[STOPT] application closed by the user.")
