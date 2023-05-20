import unittest
from unittest.mock import patch, MagicMock

from app import process_message


class TestTelegramHandlers(unittest.TestCase):
    @patch('your_module_name.ask_chatgpt')
    def test_process_message(self, mock_ask_chatgpt):
        # Mock the ask_chatgpt function
        mock_ask_chatgpt.return_value = "Response from ChatGPT"

        # Create a fake update object
        update = MagicMock()
        update.message.chat_id = 123456789
        update.message.text = "Hello, ChatGPT!"

        # Create a fake context object
        context = MagicMock()
        context.bot.send_message.return_value = None

        # Call the function to be tested
        process_message
