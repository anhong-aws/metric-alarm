# test_metric.py
import pytest
from constants import *
from moto import mock_aws
from metric_manager import MetricManager
from account_config_manager import AccountConfigManager
'''
1.运行特定测试文件：
如果您只想运行某个特定的测试文件，可以在命令行中指定该文件的路径：
pytest test_metric.py

2.运行特定测试方法：
如果您只想运行某个特定的测试方法，可以使用 -k 选项并指定方法的名称：
pytest -k test_subaccounts_and_metrics_alarm

3.标记测试：
您还可以在测试文件中使用标记（marker）来选择性地运行测试。
在测试文件中，您可以使用 @pytest.mark 来为测试方法添加标记，例如：
@pytest.mark.metric
然后，您可以使用 -m 选项来运行带有特定标记的测试：
pytest -m metric

4.全部测试
pytest
'''

@pytest.mark.metric
def test_subaccounts_and_metrics_alarm():
    accountConfigManager = AccountConfigManager()
    account_configs = accountConfigManager.read_account_configs(use_mock=True)
    metric = MetricManager(account_configs)
    metric.run()

@pytest.mark.metric_mock
@mock_aws
def test_subaccounts_and_metrics_alarm_mock():
    # Mock the assume_role call
    with mock_aws():
        accountConfigManager = AccountConfigManager()
        use_mock = True
        account_configs = accountConfigManager.read_account_configs(use_mock=use_mock)
        metric = MetricManager(account_configs)
        metric.run()