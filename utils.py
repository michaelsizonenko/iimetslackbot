
__all__ = ["extract_usernames"]


def extract_usernames(slack_users_list):
    return set([i.get("name") for i in slack_users_list])
