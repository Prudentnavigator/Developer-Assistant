'''
test_llm_models.py -- testing the llm_models module.
'''

import sys
import os
import unittest
from unittest import TestCase

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from utils_dev_assist.dev_assist_logging import app_log
    from utils_dev_assist import llm_models

except ImportError:
    pass


class LLMTest(TestCase):
    ''' Class to test the llm_models module. '''

    def setUp(self) -> None:
        ''' Logger setup. '''

        self.logger = app_log(__name__)

    def test_installed_models(self) -> None:
        ''' Tests the installed_models function. '''

        llms = llm_models.installed_models()

        if len(llms) == 0:
            self.assertEqual(len(llms), 0, "No models are installed!")

    def test_download_install_model(self) -> None:
        ''' Tests the download_install_model function. '''

        llm = "qwen2.5:0.5b"

        # Assume that the model cannot be downloaded and installed
        # successfully.
        result = llm_models.download_install_model(llm)

        self.assertIsNotNone(result, f"{llm} model download failed!")

    def test_show_model_details(self) -> None:
        ''' Tests the show_model_details function. '''

        llms = llm_models.installed_models()

        if len(llms) == 0:
            self.assertEqual(len(llms), 0, "No models are installed!")

        else:
            for idx, model in enumerate(llms):
                model = llm_models.show_model_details(idx, model)

                if len(model) == 0:
                    self.assertEqual(len(model),
                                     0,
                                     f"No details of {model} found!")

    def test_delete_model(self) -> None:
        ''' Test the delete_model function. '''

        llm = "qwen2.5:0.5b"

        # Assume that the model can be deleted successfully
        result = llm_models.delete_model(llm)

        self.assertIsNotNone(result, f"{llm} model deletion failed!")
        self.assertIn("deleted", result, f"{llm} model deletion success!")
        self.assertFalse(os.path.exists(f"./models/{llm}.tar.gz"),
                         f"{llm} model still exists after deletion!")


def main(out=sys.stderr, verbosity=2) -> None:
    """
    This function is used to run all the test cases in this module.

    Args:
        out (file object): A file object where the output will be written.
                           Defaults to sys.stderr.
        verbosity (int): Verbosity level of the test runner. Defaults to 2.

    Returns:
        None
    """

    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity=verbosity).run(suite)


if __name__ == '__main__':
    with open("test_results/llm_models_test.txt",
              "w",
              encoding="utf-8") as file:

        main(file)
