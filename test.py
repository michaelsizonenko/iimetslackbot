import unittest

from config import Config


class SlackBotTest(unittest.TestCase):

    def test_config(self):
        config = Config()
        self.assertIsNotNone(config.department_id)
        self.assertIsNotNone(config.slack_client_token)
        self.assertIsNotNone(config.slack_bot_token)
        self.assertIsNotNone(config.ticket_id_delivery_channel)


if __name__ == "__main__":
    unittest.main()
