import unittest
import os
import validators

from config import Config


class SlackBotTest(unittest.TestCase):

    def test_config(self):
        config = Config()
        self.assertIsNotNone(config.department_id)
        self.assertIsNotNone(config.slack_client_token)
        self.assertIsNotNone(config.slack_bot_token)
        self.assertIsNotNone(config.ticket_id_delivery_channel)
        self.assertIsNotNone(config.sheet_url)
        self.assertTrue(validators.url(config.sheet_url))
        self.assertRegex(config.sheet_url, r"/spreadsheets/d/([a-zA-Z0-9-_]+)")
        self.assertRegex(config.sheet_url, r"[#&]gid=([0-9]+)")
        self.assertIsNotNone(config.spreadsheet_id)
        self.assertIsNotNone(config.sheet_id)

    @unittest.skip("later")
    def test_google_sheet_wrapper(self):
        config = Config()
        self.assertTrue(os.path.exists("credentials.json"))
        self.assertTrue(config.sheet_url)
        from google_sheet_wrapper import google_sheet_wrapper
        self.assertIsNotNone(google_sheet_wrapper.get_data())


if __name__ == "__main__":
    unittest.main()
