import unittest
import os
from unittest.mock import Mock, patch

from app import (
    authenticate_secret_token,
    process_message,
    process_voice_message,
)

# Telegram token
TO_TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
FROM_TELEGRAM_TOKEN = os.environ["TELEGRAM_SECRET_TOKEN"]

# Open API Token
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


class YourTestCase(unittest.TestCase):
    def test_authenticate_secret_token(self):
        # Test with valid secret token
        valid_token = "valid_token"
        self.assertTrue(authenticate_secret_token(valid_token))

        # Test with invalid secret token
        invalid_token = "invalid_token"
        self.assertFalse(authenticate_secret_token(invalid_token))

    def test_process_message(self):
        # Mock the necessary objects
        mock_update = Mock()
        mock_context = Mock()

        # Test the process_message function
        with patch("app.ask_chatgpt") as mock_ask_chatgpt:
            mock_ask_chatgpt.return_value = "Mock response"
            process_message(mock_update, mock_context)

            # Assert the expected behavior
            mock_ask_chatgpt.assert_called_once_with(mock_update.message.text)
            mock_context.bot.send_message.assert_called_once_with(
                chat_id=mock_update.message.chat_id,
                text="Mock response",
                parse_mode="Markdown",
            )

    def test_process_voice_message(self):
        # Mock the necessary objects
        mock_update = Mock()
        mock_context = Mock()

        # Test the process_voice_message function
        process_voice_message(mock_update, mock_context)

        # Assert the expected behavior
        mock_context.bot.send_message.assert_called_once_with(
            chat_id=mock_update.message.chat_id,
            text="Voice Messages are currently not supported.",
            parse_mode="Markdown",
        )


if __name__ == "__main__":
    unittest.main()
