from slackclient import SlackClient
import logging

class Slack():
    def __init__(self, config):
        self.config = config
        self.slack_client = SlackClient(self.config.user_alert_slack_token) if self.config.user_alert_enabled else None
        self.users_list = None

    def refresh_userlist(self):
        if self.slack_client is None:
            return False
        response = self.slack_client.api_call('users.list')
        if 'members' not in response:
            logging.warning('Cannot refresh slack user list')
            return False
        self.users_list = response['members']

    def get_userid(self, identifier):
        if self.users_list is None:
            return False
        user = next((user for user in self.users_list if user['profile']['display_name_normalized'] == identifier), None)
        return user['id'] if user else False
        
    def send_alert(self, identifier, message):
        if self.slack_client is None:
            return False
        userid = self.get_userid(identifier)
        if not userid:
            return False
        self.slack_client.api_call("chat.postMessage", channel=userid, text=message)

    
