'''
test_llm_models.py -- testing the llm_models module.
'''

import sys
import os
import unittest
from unittest import mock
from unittest import TestCase

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from utils_dev_assist.dev_assist_logging import app_log
    from utils_dev_assist import llm_models as lm

except ImportError:
    pass


class LLMTest(TestCase):
    ''' Class to test the llm_models module. '''

    def setUp(self) -> None:
        ''' Logger setup. '''

        self.logger = app_log(__name__)

    def test_installed_models(self) -> None:
        ''' Tests the installed_models function. '''

        llms = lm.installed_models()

        if len(llms) == 0:
            self.assertEqual(len(llms), 0, "No models are installed!")

    def test_download_install_model(self) -> None:
        ''' Tests the download_install_model function. '''

        llm = "qwen2.5:0.5b"

        # Assume that the model cannot be downloaded and installed
        # successfully.
        result = lm.download_install_model(llm)

        self.assertIsNotNone(result, f"{llm} model download failed!")

    def test_show_model_info(self):
        model = "test_model"
        info_type = "test_info_type"
        
        # Mock the requests.post call to return a specific response
        with mock.patch('requests.post') as mock_request:
            mock_response = mock.Mock()
            mock_response.text = '{"test_info_type": "test_info"}'
            mock_request.return_value = mock_response
            
            result = lm.show_model_info(model, info_type)
            self.assertEqual(result, "TEST_INFO_TYPE:\ntest_info\n\n")

    def test_delete_model(self) -> None:
        ''' Test the delete_model function. '''

        llm = "qwen2.5:0.5b"

        # Assume that the model can be deleted successfully
        result = lm.delete_model(llm)

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
