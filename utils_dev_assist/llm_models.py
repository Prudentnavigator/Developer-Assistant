#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
llm_modules.py-This module checks for installed models, downloads, shows info
               and deletes models.
'''

import os
import json
import requests
import ollama
from utils_dev_assist.dev_assist_logging import app_log

logger = app_log(__name__)


def installed_models() -> list:
    '''
    Returns a list of installed LLM's.
    '''

    models = []
    model_list = ollama.list()

    if len(model_list.models) == 0:
        logger.info(" [LLM] --> No models are installed! <--")

    else:
        for idx, model in enumerate(model_list.models):
            models.append(model["model"])
            qty_of_models = idx + 1

        logger.info(" [LLM] %s models are installed! ", qty_of_models)

        return models

    return "\n --> No models are installed! <-- \n\n"


def download_install_model(model: str) -> str:
    '''
    Downloads and installs models.
    '''

    try:
        logger.info(" [LLM] starting download of model --> %s ...", model)
        ollama.pull(model)
        logger.info(" download of model: %s --> success!", model)
        msg = f"Model: {model} has been downloaded and installed!"
        return f"--> {msg}  <--"

    except ollama._types.ResponseError as error:
        logger.error(" [LLM] download of model --> %s failed!", model)
        logger.error(" --> %s", error.error)
        error_msg = error.error.split("/")

        if error.status_code == 500:
            if "no such host" in error.error:
                msg = f"download of the model {model} failed!"
                return f"{msg}\nIt appears that your device is offline!"

            msg = f"download of the model {model} failed!"
            return f"{msg}\n{error.error}"

        return f"{error_msg[0]}!"


def show_model_info(model: str, info_type: str) -> str:
    '''
    Displays the information of a LLM.
    '''

    url = "http://localhost:11434/api/show"

    data = {"model": model}

    try:
        info = ""
        info_list = []
        info_type = info_type.upper()

        res = requests.post(url, json=data, timeout=(5, None))
        res_json = json.loads(res.text)

        for key, item in res_json.items():
            if key.upper() == info_type:
                info_list.append(str(item))

        info = info.join(info_list)

        if info == "":
            msg = " [LLM] %s for %s is empty!"
            logger.debug(msg, info_type, model)
            return f"\n {model} --> {info_type} appears to be empty!\n\n"

        msg = " [LLM] Displaying %s for model --> %s!"
        logger.debug(msg, info_type, model)

        return f" {info_type}:\n{info}\n\n"

    except Exception as error:
        msg = " [LLM] Failed to display %s for model --> %s!"
        logger.error(msg, info_type, model)
        logger.error("--> %s", error)
        return f"[ERROR] --> {error}\n\n"


def create_model(new_model: str, new_modelfile: str) -> str:
    """
    Creates a new model.
    """

    # Create the path to a new modelfile with the given name from 'new_model'.
    modelfile = f"utils_dev_assist/modelfile_{new_model}"

    # Write the modelfile.
    with open(modelfile, "w", encoding="utf-8") as modfile:
        modfile.write(new_modelfile)

    logger.debug(" [LLM] a new modelfile %s has been written!", modelfile)

    try:
        # Create the model using 'ollama' command line tool.
        os.system(f"'ollama' 'create' '{new_model}' '-f' '{modelfile}'")
        logger.info(" [LLM] model -> %s has been created!", new_model)
        return f" Model: {new_model} has been created!"

    except Exception as error:
        # Return an error message if any exception occurs during the
        # creation process.
        logger.error(" [LLM] model -> %s creation has failed!", new_model)
        logger.error(" [LLM-ERROR] -> %s", error)
        return f"[ERROR] {error}"


def help_create_model() -> str:
    '''
    Returns the contents of 'modelfile_help.txt' located in the assets
    directory, which is a subdirectory of the main script's directory.
    '''

    # Get the parent dir for the parent dir of current file's location.
    path = os.path.dirname(os.path.dirname(__file__))

    # Construct full path for the file.
    help_file = f"{path}/assets/modelfile_help.txt"

    try:
        with open(help_file, "r", encoding="utf-8") as infile:
            help_txt = infile.read()

        logger.info(" [LLM] modelfile help text returned to GUI.")
        return help_txt

    except FileNotFoundError:
        logger.warning(" [LLM] %s Not Found!", help_file)
        return f"\n {help_file} not found!"


def delete_model(model: str) -> bool:
    '''
    Deletes the loaded model.
    '''

    # If the model was created by the user, delete the modelfile.
    modelfile_name = f"modelfile_{model[:-7]}"
    modelfile_dir = os.path.dirname(__file__)
    modelfile = f"{modelfile_dir}/{modelfile_name}"

    if os.path.isfile(modelfile):
        os.remove(modelfile)
        logger.info(" modelfile of: %s --> deleted!", model)

    # Delete the model.
    ollama.delete(model)

    logger.info(" model: %s --> deleted!", model)

    return True
