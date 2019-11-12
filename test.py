import unittest
import os

from clock_row_model import ClockRowItem
from main_logger import logger
from utils import extract_usernames
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
        self.assertIsNotNone(config.range)

    def test_google_sheet_wrapper(self):
        config = Config()
        self.assertTrue(os.path.exists("credentials.json"))
        self.assertTrue(config.sheet_url)
        from google_sheet_wrapper import google_sheet_wrapper
        test_data = google_sheet_wrapper.get_existed_data()
        self.assertIsNotNone(test_data)
        test_slack_users_list = [
            {'id': 'USLACKBOT', 'team_id': 'TQ5DL0TQC', 'name': 'slackbot', 'deleted': False, 'color': '757575',
             'real_name': 'Slackbot', 'tz': None, 'tz_label': 'Pacific Standard Time', 'tz_offset': -28800,
             'profile': {'title': '', 'phone': '', 'skype': '', 'real_name': 'Slackbot',
                         'real_name_normalized': 'Slackbot', 'display_name': 'Slackbot',
                         'display_name_normalized': 'Slackbot', 'fields': None, 'status_text': '', 'status_emoji': '',
                         'status_expiration': 0, 'avatar_hash': 'sv41d8cd98f0', 'always_active': True,
                         'first_name': 'slackbot', 'last_name': '',
                         'image_24': 'https://a.slack-edge.com/80588/img/slackbot_24.png',
                         'image_32': 'https://a.slack-edge.com/80588/img/slackbot_32.png',
                         'image_48': 'https://a.slack-edge.com/80588/img/slackbot_48.png',
                         'image_72': 'https://a.slack-edge.com/80588/img/slackbot_72.png',
                         'image_192': 'https://a.slack-edge.com/80588/marketing/img/avatars/slackbot/avatar-slackbot.png',
                         'image_512': 'https://a.slack-edge.com/80588/img/slackbot_512.png',
                         'status_text_canonical': '', 'team': 'TQ5DL0TQC'}, 'is_admin': False, 'is_owner': False,
             'is_primary_owner': False, 'is_restricted': False, 'is_ultra_restricted': False, 'is_bot': False,
             'is_app_user': False, 'updated': 0},
            {'id': 'UQ2NX7WHX', 'team_id': 'TQ5DL0TQC', 'name': 'formtestbot', 'deleted': False, 'color': '3c989f',
             'real_name': 'formtestbot', 'tz': 'America/Los_Angeles', 'tz_label': 'Pacific Standard Time',
             'tz_offset': -28800, 'profile': {'title': '', 'phone': '', 'skype': '', 'real_name': 'formtestbot',
                                              'real_name_normalized': 'formtestbot', 'display_name': '',
                                              'display_name_normalized': '', 'status_text': '', 'status_emoji': '',
                                              'status_expiration': 0, 'avatar_hash': 'gea267e42fb4',
                                              'api_app_id': 'AQAKUH940', 'always_active': False, 'bot_id': 'BPXSTE202',
                                              'image_24': 'https://secure.gravatar.com/avatar/ea267e42fb458d5c5df5f0a9f4db65ba.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0013-24.png',
                                              'image_32': 'https://secure.gravatar.com/avatar/ea267e42fb458d5c5df5f0a9f4db65ba.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0013-32.png',
                                              'image_48': 'https://secure.gravatar.com/avatar/ea267e42fb458d5c5df5f0a9f4db65ba.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0013-48.png',
                                              'image_72': 'https://secure.gravatar.com/avatar/ea267e42fb458d5c5df5f0a9f4db65ba.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0013-72.png',
                                              'image_192': 'https://secure.gravatar.com/avatar/ea267e42fb458d5c5df5f0a9f4db65ba.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0013-192.png',
                                              'image_512': 'https://secure.gravatar.com/avatar/ea267e42fb458d5c5df5f0a9f4db65ba.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0013-512.png',
                                              'status_text_canonical': '', 'team': 'TQ5DL0TQC'}, 'is_admin': False,
             'is_owner': False, 'is_primary_owner': False, 'is_restricted': False, 'is_ultra_restricted': False,
             'is_bot': True, 'is_app_user': False, 'updated': 1573196943},
            {'id': 'UQ5DL0V5J', 'team_id': 'TQ5DL0TQC', 'name': 'michael.sizonenko.17', 'deleted': False,
             'color': '9f69e7', 'real_name': 'Michael Sizonenko', 'tz': 'Asia/Jerusalem',
             'tz_label': 'Israel Standard Time', 'tz_offset': 7200,
             'profile': {'title': '', 'phone': '', 'skype': '', 'real_name': 'Michael Sizonenko',
                         'real_name_normalized': 'Michael Sizonenko', 'display_name': '', 'display_name_normalized': '',
                         'status_text': '', 'status_emoji': '', 'status_expiration': 0, 'avatar_hash': 'g29a5bc9023f',
                         'first_name': 'Michael', 'last_name': 'Sizonenko',
                         'image_24': 'https://secure.gravatar.com/avatar/29a5bc9023fb554ad6dcdede2a7fabe8.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-24.png',
                         'image_32': 'https://secure.gravatar.com/avatar/29a5bc9023fb554ad6dcdede2a7fabe8.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-32.png',
                         'image_48': 'https://secure.gravatar.com/avatar/29a5bc9023fb554ad6dcdede2a7fabe8.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-48.png',
                         'image_72': 'https://secure.gravatar.com/avatar/29a5bc9023fb554ad6dcdede2a7fabe8.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-72.png',
                         'image_192': 'https://secure.gravatar.com/avatar/29a5bc9023fb554ad6dcdede2a7fabe8.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-192.png',
                         'image_512': 'https://secure.gravatar.com/avatar/29a5bc9023fb554ad6dcdede2a7fabe8.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-512.png',
                         'status_text_canonical': '', 'team': 'TQ5DL0TQC'}, 'is_admin': True, 'is_owner': True,
             'is_primary_owner': True, 'is_restricted': False, 'is_ultra_restricted': False, 'is_bot': False,
             'is_app_user': False, 'updated': 1572956970, 'has_2fa': False},
            {'id': 'UQ5TGKNCD', 'team_id': 'TQ5DL0TQC', 'name': 'dethline88', 'deleted': False, 'color': '4bbe2e',
             'real_name': 'Dethline', 'tz': 'Asia/Jerusalem', 'tz_label': 'Israel Standard Time', 'tz_offset': 7200,
             'profile': {'title': '', 'phone': '', 'skype': '', 'real_name': 'Dethline',
                         'real_name_normalized': 'Dethline', 'display_name': 'Dethline',
                         'display_name_normalized': 'Dethline', 'status_text': '', 'status_emoji': '',
                         'status_expiration': 0, 'avatar_hash': 'g1a3120f3fa3',
                         'image_24': 'https://secure.gravatar.com/avatar/1a3120f3fa31b374a86900fe525d0af8.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0009-24.png',
                         'image_32': 'https://secure.gravatar.com/avatar/1a3120f3fa31b374a86900fe525d0af8.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0009-32.png',
                         'image_48': 'https://secure.gravatar.com/avatar/1a3120f3fa31b374a86900fe525d0af8.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0009-48.png',
                         'image_72': 'https://secure.gravatar.com/avatar/1a3120f3fa31b374a86900fe525d0af8.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0009-72.png',
                         'image_192': 'https://secure.gravatar.com/avatar/1a3120f3fa31b374a86900fe525d0af8.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0009-192.png',
                         'image_512': 'https://secure.gravatar.com/avatar/1a3120f3fa31b374a86900fe525d0af8.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0009-512.png',
                         'status_text_canonical': '', 'team': 'TQ5DL0TQC'}, 'is_admin': False, 'is_owner': False,
             'is_primary_owner': False, 'is_restricted': False, 'is_ultra_restricted': False, 'is_bot': False,
             'is_app_user': False, 'updated': 1572953382, 'has_2fa': False},
            {'id': 'UQ845012A', 'team_id': 'TQ5DL0TQC', 'name': 'testbot', 'deleted': False, 'color': 'e7392d',
             'real_name': 'testbot', 'tz': 'America/Los_Angeles', 'tz_label': 'Pacific Standard Time',
             'tz_offset': -28800, 'profile': {'title': '', 'phone': '', 'skype': '', 'real_name': 'testbot',
                                              'real_name_normalized': 'testbot', 'display_name': '',
                                              'display_name_normalized': '', 'status_text': '', 'status_emoji': '',
                                              'status_expiration': 0, 'avatar_hash': 'ge69d54dab8b',
                                              'api_app_id': 'APY0FKYHF', 'always_active': False, 'bot_id': 'BPT48B01G',
                                              'image_24': 'https://secure.gravatar.com/avatar/e69d54dab8bf407554da095a3b8cf969.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-24.png',
                                              'image_32': 'https://secure.gravatar.com/avatar/e69d54dab8bf407554da095a3b8cf969.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-32.png',
                                              'image_48': 'https://secure.gravatar.com/avatar/e69d54dab8bf407554da095a3b8cf969.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-48.png',
                                              'image_72': 'https://secure.gravatar.com/avatar/e69d54dab8bf407554da095a3b8cf969.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-72.png',
                                              'image_192': 'https://secure.gravatar.com/avatar/e69d54dab8bf407554da095a3b8cf969.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-192.png',
                                              'image_512': 'https://secure.gravatar.com/avatar/e69d54dab8bf407554da095a3b8cf969.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-512.png',
                                              'status_text_canonical': '', 'team': 'TQ5DL0TQC'}, 'is_admin': False,
             'is_owner': False, 'is_primary_owner': False, 'is_restricted': False, 'is_ultra_restricted': False,
             'is_bot': True, 'is_app_user': False, 'updated': 1572953111}]
        self.assertSetEqual({'michael.sizonenko.17', 'formtestbot', 'dethline88', 'slackbot', 'testbot'}, extract_usernames(test_slack_users_list))
        with self.assertRaises(Exception):
            test_user_data = google_sheet_wrapper.get_data_by_user("test")
        test_user_data = google_sheet_wrapper.get_data_by_user('michael.sizonenko.17')
        empty_row_model = ClockRowItem()
        self.assertEqual(test_user_data, empty_row_model)


if __name__ == "__main__":
    logger.debug("This is a debug message.")
    unittest.main()
