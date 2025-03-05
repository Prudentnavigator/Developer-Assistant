(ins)***Developer Assistant v1.0.0***(/ins)

This application provides a GUI to interact with LLM's (large language models) that are installed locally with Ollama python API.\
It allows users to submit requests, receive responses, and attach files to their requests.\
The application uses customtkinter for its design and supports
multiple appearance modes and scaling options. 


***Installation and setup:***
- Install Ollama for your platform.
  https://ollama.com/download
- Search for a model.
  https://ollama.com/search
- Download a model from the CLI
  i.e; ollama pull wizardcoder\
  or models can also be downloaded    from the app.

> [!TIP]
> Ensure that the ollama server is    running.
> In general, larger models will take longer to respond than smaller models.\
> Would recommend to download multiple models and try them out.

***Usage:***
1. Start by running the script and load a language model by selecting it
   from the dropdown menu ("choose model" button).
2. Enter your request in the text entry field. Attach a text file with the
   "attach file" button to add to the request (optional).
   A text can also be pasted into the text entry field (i.e. a code snippet)
   from the clipboard by using keyboard shortcuts (ctrl-v for linux).
3. Submit the request using the "Submit" button.
4. Receive a response from the LLM, which will be displayed in the reply textbox.

***Requirements:***
- python3.8 or higher 
- Install packages (see requirements.txt).

***Hardware Requirements:***
- A modern CPU with at least 4 cores.
- GPU acceleration (optional but recommended for larger models).

***Features:***
- Confirmation and error messages are displayed in the GUI.
- Logs are written to the '.dev_assist.log' file on a          rotating basis (max 3 files).
- Downloading models.
- View details of the loaded model.
- Delete models.
- Change GUI appearance.
- Change GUI scaling.

***Contributing:***\
Contributions are very welcome!\
Please feel free to open an issue or create a pull request if you have any suggestions for improvements or want to contribute new features. 

***SUPPORT/CONTACT:***\
If you have any questions, need help or want to report a bug, please feel free
to contact me at tommy_software@mailfence.com.
