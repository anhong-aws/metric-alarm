# from constants import *
# from sts_manager import STSManager
# from cloud_front_manager import CloudFrontManager
# from cloudwatch import get_metric_statistics
# from sns_main import run_sns_operations
# from alarm_manager import AlarmManager
# from helper_utils import HelperUtils

# from account_config_manager import AccountConfigManager

# class DataCollector:
#     def __init__(self, account_configs):
#         self.account_configs = account_configs
#         self.sts = STSManager()
        
#     def collect_data(self):
#         # print(f"account_configs1:{self.account_configs}")
#         # 返回每个账号下的指标
#         for config in self.account_configs:
#             # print(config)
#             assumed_role_credentials = self.sts.get_assumed_role_credentials(config[ACCOUNT_ID], config[ROLE])
#             cf = CloudFrontManager(assumed_role_credentials)
#             distributions = cf.list_deployed_distributions()
#             # print(distributions)
#             for distribution in distributions:
#                 metric_statistics = get_metric_statistics(assumed_role_credentials, distribution, config[MINUTES], config[PERIOD], SUM)
#                 print(f"---{distribution['Id']}:{metric_statistics}")
#                 # self.metricSummary.create_or_update_item
#                 # yield distribution, metric_statistics, config



# accountConfigManager = AccountConfigManager()
# account_configs = accountConfigManager.read_account_configs(use_mock=True)
# print(f"account_configs:{account_configs}")
# d = DataCollector(account_configs)
# d.collect_data()
