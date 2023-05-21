import unittest
import os
from unittest.mock import MagicMock, patch
from app import (
    ask_chatgpt,
    process_message,
    process_voice_message,
    authenticate_secret_token,
    message_handler,
)

# Telegram token
TO_TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
FROM_TELEGRAM_TOKEN = os.environ["TELEGRAM_SECRET_TOKEN"]

# Open API Token
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

class AppTests(unittest.TestCase):
    def test_ask_chatgpt(self):
        # Mock the openai.ChatCompletion.create function
        with patch("openai.ChatCompletion.create") as mock_create:
            mock_create.return_value = {
                "choices": [
                    {
                        "message": {
                            "content": "Response from ChatGPT"
                        }
                    }
                ]
            }
            response = ask_chatgpt("Hello")
            self.assertEqual(response, "Response from ChatGPT")

    def test_process_message(self):
        # Mock the context.bot.send_message function
        with patch("context.bot.send_message") as mock_send_message:
            process_message(None, MagicMock(), chat_text="Hello")
            mock_send_message.assert_called_once_with(
                chat_id=None,
                text="Response from ChatGPT",
                parse_mode="Markdown",
            )

    def test_process_voice_message(self):
        # Mock the context.bot.send_message function
        with patch("context.bot.send_message") as mock_send_message:
            process_voice_message(None, MagicMock())
            mock_send_message.assert_called_once_with(
                chat_id=None,
                text="Voice Messages are currently not supported.",
                parse_mode="Markdown",
            )

    def test_authenticate_secret_token(self):
        # Test with a valid secret token
        self.assertTrue(authenticate_secret_token(FROM_TELEGRAM_TOKEN))

        # Test with an invalid secret token
        self.assertFalse(authenticate_secret_token("invalid_secret_token"))

    def test_message_handler(self):
        # Mock the Update.de_json function and other dependencies
        with patch("Update.de_json"), \
             patch("dispatcher.process_update") as mock_process_update:
            # Mock the authenticate_secret_token function
            with patch("__main__.authenticate_secret_token") as mock_authenticate:
                mock_authenticate.return_value = True
                event = {
                    "headers": {
                        "X-Telegram-Bot-Api-Secret-Token": FROM_TELEGRAM_TOKEN
                    },
                    "body": "{}"
                }
                response = message_handler(event, None)
                self.assertEqual(response, {"statusCode": 200})
                mock_process_update.assert_called_once()

            # Test with an invalid secret token
            with patch("__main__.authenticate_secret_token") as mock_authenticate:
                mock_authenticate.return_value = False
                event = {
                    "headers": {
                        "X-Telegram-Bot-Api-Secret-Token": "invalid_secret_token"
                    },
                    "body": "{}"
                }
                response = message_handler(event, None)
                self.assertEqual(response, {"statusCode": 403})


if __name__ == "__main__":
    unittest.main()
