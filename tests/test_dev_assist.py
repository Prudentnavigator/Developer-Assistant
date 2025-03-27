'''
test_dev_assist.py--tests the dev_assist.py module.
'''

import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from utils_dev_assist.dev_assist_logging import app_log
    from utils_dev_assist import dev_assist as da

except ImportError:
    pass


class TestDevAssist(unittest.TestCase):
    '''
    Class for testing the functions of the dev_assist.py module.
    '''

    def setUp(self) -> None:
        ''' Setup. '''

        self.logger = app_log(__name__)

    def test_create_message(self) -> None:
        '''
        Tests the create_message() function with valid and invalid inputs.

        Args:
            None

        Returns:
            None
        '''

        # Testing with invalid inputs.
        message1 = "Hello, how can I help you?"
        role1 = "user"

        self.assertEqual(da.create_message(message1, role1),
                         {'role': 'user',
                          'content': 'Hello!'})

        # Testing with invalid inputs.
        message2 = ""
        role2 = "assistant"

        self.assertEqual(da.create_message(message2, role2),
                         {'role': 'assistant', 'content': ''})

    def test_chat(self) -> None:
        '''
        Tests the chat() function with valid inputs.

        Args:
            None

        Returns:
            None
        '''

        # Testing with valid inputs.
        llm = "wizardcoder"

        self.assertIsInstance(da.chat(llm), str)

        # Testing with invalid inputs.
        llm1 = ""

        self.assertIsNot(da.chat(llm1),
                         "\n\n[Error]  -->  Model name is required!")

    def test_ask(self) -> None:
        '''
        Tests the ask() function with valid and invalid inputs.

        Args:
            None

        Returns:
            None
        '''

        # Testing with valid inputs.
        query = "What is a class in Python?"
        llm1 = "wizardcoder"

        parent_dir = os.path.dirname(__file__)
        add_file = f"{parent_dir}/text_test.txt"

        self.assertIsInstance(da.ask(query, llm1, add_file), str)

        # Testing with invalid inputs.
        query1 = ""
        llm2 = ""
        add_file = ""

        self.assertIsNot(da.ask(query1, llm2, add_file),
                         "\n\n[Error]  -->  Please provide a valid query!")

    def test_app_log(self):
        '''
        Tests the app_log() function with valid inputs.

        Args:
            None

        Returns:
            None
        '''

        logger = app_log(__name__)

        self.assertIsInstance(logger, object)


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
    # Create an instance of a TestLoader object, which is responsible for
    # discovering and loading tests from modules.
    loader = unittest.TestLoader()

    # Load all the test cases from the current module.
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    # Run the test suite using a TextTestRunner object.
    unittest.TextTestRunner(out, verbosity=verbosity).run(suite)


if __name__ == '__main__':
    with open("test_results/dev_assist_test.txt",
              "w", encoding="utf-8") as file:
        main(file)
