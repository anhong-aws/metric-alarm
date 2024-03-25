import os
from constants import *
from ddb_account_metric_config_items import DdbAccountMetricConfigItems

class AccountConfigManager:
    def __init__(self):
        """
        Initializes the Account Config Manager.
        """
        self.metric_table = DdbAccountMetricConfigItems()

    def get_mock_account_config(self):
        """
        Returns a mock account configuration for testing purposes.

        :return: A dictionary containing mock account configuration details.
        """
        return {
            'account_id': os.getenv('MOCK_ACCOUNT_ID', '123'),
            'account_name': os.getenv('MOCK_ACCOUNT_NAME', 'demo'),
            'role': 'OrganizationAccountAccessRole',
            'status': Status.OPEN.value,
            'consecutive_points': 1,
            'threshold': 1,
            'period': 300,
            'minutes': 30,
            "auto_disable_service_threshold": 500000,
            "auto_disable_service_flag": Status.OPEN.value,
            'send_sns_flag': Status.OPEN.value,
            'payer_topic_name': 'metric-alarm-topic',
            'send_linked_sns_flag': Status.CLOSE.value,
            'linked_topic_name': 'metric-alarm-topic'+os.getenv('MOCK_ACCOUNT_ID', '123'),
            'telegram_info': {
                'send_flag': Status.OPEN.value,
                "webhook": os.getenv('TELEGRAM_URL', 'https://'),
                "chat_id": "-4194166355"
            },
            'lark_info': {
                'send_flag': Status.OPEN.value,
                "webhook": os.getenv('LARK_URL', 'https://'),
            },
            'dingding_info': {
                'send_flag': Status.OPEN.value,
                "webhook": os.getenv('DINGDING_URL', 'https://'),
            },
            'linked_telegram_info': {
                'send_flag': "close",
                "webhook": os.getenv('TELEGRAM_URL', 'https://'),
                "chat_id": ""
            },
            'linked_lark_info': {
                'send_flag': "close",
                "webhook": ""
            },
            'linded_dingding_info': {
                'send_flag': "close",
                "webhook": ""
            },
            "use_mock": True,
        }

    def read_account_configs(self, use_mock=False):
        """
        Reads account configurations from the DynamoDB table.

        :param use_mock: If True, use mock data; otherwise, read from the table.
        :return: A list of dictionaries containing account configurations.
        """
        if use_mock:
            return [self.get_mock_account_config()]
        else:
            try:
                return self.metric_table.read_item_by_status()
            except Exception as e:
                print(f"Error reading account configurations: {e}")
                return []

    # Other methods (add, update, delete) can remain unchanged

# Example usage
if __name__ == "__main__":
    account_manager = AccountConfigManager()

    # Read account configurations using mock data
    account_configs_mock = account_manager.read_account_configs(use_mock=True)
    if account_configs_mock:
        print("Read mock account configurations:", account_configs_mock)
    else:
        print("No mock account configurations found.")

    # Read account configurations from the table
    account_configs_table = account_manager.read_account_configs(use_mock=False)
    if account_configs_table:
        print("Read account configurations from the table:", account_configs_table)
    else:
        print("No account configurations found in the table.")
