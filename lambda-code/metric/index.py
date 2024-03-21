# index.py
from account_config_manager import AccountConfigManager
from metric_manager import MetricManager


def handler(event, context):
    accountConfigManager = AccountConfigManager()
    account_configs = accountConfigManager.read_account_configs()
    metricManager = MetricManager()
    metricManager.run(account_configs)