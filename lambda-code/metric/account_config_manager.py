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
            'period': 300,
            'minutes': 30,
            'threshold': 1,
            'consecutive_points': 1,
            'payer_topic_name': 'metric-alarm-topic',
            'status': Status.OPEN.value,
            'send_sns_flag': Status.OPEN.value,
            # 'send_linked_sns_flag': Status.CLOSE.value,
            # 'save_metric_log_flag': Status.OPEN.value,
            "auto_disable_service_threshold": 500000,
            # "max_request_multiple": 5,
            "auto_disable_service_flag": Status.OPEN.value,
            "use_mock": True,
            # "aws_services":[
            #     {
            #         "name": "cf",
            #         "auto_disable_service_flag": Status.OPEN,
            #     },
            #     {
            #         "name": "alb",
            #         "auto_disable_service_flag": Status.OPEN,
            #     }
            # ]
            # ,'payer_email_addresses' : ['jarrywen@163.com', 'jarrywenjack@gmail.com']
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
