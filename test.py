import unittest
import os

from config import Config


class SlackBotTest(unittest.TestCase):

    def test_config(self):
        config = Config()
        self.assertIsNotNone(config.department_id)
        self.assertIsNotNone(config.slack_client_token)
        self.assertIsNotNone(config.slack_bot_token)
        self.assertIsNotNone(config.ticket_id_delivery_channel)

    def test_google_sheet_wrapper(self):
        config = Config()
        self.assertTrue(os.path.exists("credentials.json"))
        self.assertTrue(config.sheet)
        from google_sheet_wrapper import google_sheet_wrapper


if __name__ == "__main__":
    unittest.main()
