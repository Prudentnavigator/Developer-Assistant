#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2025

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
llm_modules.py-This module checks for installed, downloads, shows info
and deletes LLM's (Large Language Model's).
'''

import ollama
from utils_dev_assist.dev_assist_logging import app_log

logger = app_log(__name__)


def installed_models() -> list:
    '''
    Functon returns a list of installed LLM's

    Parameters:
        None

    Returns:
        llm: A list of installed models.
    '''

    llms = []
    model_list = ollama.list()

    if len(model_list.models) == 0:
        logger.info(" [LLM] --> No models are installed! <--")

    else:
        for idx, llm in enumerate(model_list.models):
            llms.append(llm["model"])
            amount_of_models = idx + 1

        logger.info(" [LLM] %s models are installed! ", amount_of_models)

        return llms

    return "\n --> No models are installed! <-- \n\n"


def download_install_model(llm: str) -> None | str:
    '''
    Function to download and install a LLM.

    Parameters:
        llm (str): The name of a language model to download.

    Returns:
        None
        str: Send a message to the GUI that the download as failed.
    '''

    try:
        ollama.pull(llm)
        logger.info(" [LLM] starting download of model --> %s ...", llm)

    except Exception as error:
        logger.error(" [LLM] download of model --> %s failed!", llm)
        logger.error(" --> %s", error)
        msg = "download of the model {llm} failed!"
        return f"\n[ERROR] --> {msg}  \n--> {error}\n\n"

    else:
        logger.info(" download of model: %s --> success!", llm)
        return f"\n--> Model: {llm} has been downloaded and installed! <--\n\n"


def show_model_details(llm: int, model: None) -> str:
    '''
    Function to display the details of a LLM.

    Parameters:
        llm (int): The index of a model returned from the installed_models()
                   list to display details for.
        model (str): Model name returned from the installed_models() list to
                     display details for.

    Returns:
        str: A string containing the model's name and its details.
    '''

    info = ollama.list()

    try:
        model_name = info.models[llm].model
        model_details = info.models[llm].details

        logger.debug(" [LLM] Displaying details for model --> %s!", model)

        return f"Model name:\n{model_name}\n\nDetails:\n{model_details}\n\n"

    except Exception as error:
        logger.error(" [LLM] Failed to display details for model --> %s!", llm)
        logger.error("--> %s", error)
        return f"[ERROR] --> {error}\n\n"


def delete_model(llm: str) -> str:
    '''
    Deletes an installed model.

    Arg:
        llm (str): The name of the model to delete.

    Returns:
        str: Sends a message to the GUI to let the user know that the LLM
             has been deleted.
    '''

    ollama.delete(llm)

    logger.info(" model: %s --> deleted!", llm)

    return f"\n--> model: {llm} has been deleted! <--\n"
