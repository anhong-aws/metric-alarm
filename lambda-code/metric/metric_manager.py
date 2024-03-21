from constants import *
from sts_manager import STSManager
from cloud_front_manager import CloudFrontManager
from cloudwatch import get_metric_statistics
from sns_main import run_sns_operations
from alarm_manager import AlarmManager
from helper_utils import HelperUtils

class DataCollector:
    def __init__(self, account_configs):
        self.account_configs = account_configs
        self.sts = STSManager()
        
    def format(self, metric_statistics):
        all_metrics = []
        max_sum = float('-inf')  # Initialize max_sum to negative infinity to start tracking the maximum
        for point in metric_statistics['Datapoints']:
            all_metrics.append({
                'StartTime': metric_statistics['StartTime'],
                'EndTime': metric_statistics['EndTime'],
                'sum': point[SUM]
            })
            if point[SUM] > max_sum:
                max_sum = point[SUM]  # Update max_sum if the current sum is greater

        return all_metrics, max_sum
    def collect_data(self):
        # 返回每个账号下的指标
        for config in self.account_configs:
            assumed_role_credentials = self.sts.get_assumed_role_credentials(config[ACCOUNT_ID], config[ROLE])
            cf = CloudFrontManager(assumed_role_credentials)
            distributions = cf.list_deployed_distributions()
            for distribution in distributions:
                metric_statistics = get_metric_statistics(assumed_role_credentials, distribution, config[MINUTES], config[PERIOD], SUM)
                # self.metricSummary.create_or_update_item
                yield distribution['Id'], metric_statistics, config, assumed_role_credentials

class PointEvaluator:
    def __init__(self, config):
        self.config = config
        self.consecutive_points = config[CONSECUTIVE_POINTS]
        
    def evaluate_for_disable(self, metric_statistics, threshold):
        if self.config[AUTO_DISABLE_SERVICE_FLAG] == Status.OPEN.value:
            consecutive_high_points = 0
            for point in metric_statistics['Datapoints']:
                if point[SUM] >= threshold:
                    consecutive_high_points += 1
                else:
                    consecutive_high_points = 0

                if consecutive_high_points >= self.consecutive_points:
                    return True
        return False

    def evaluate(self, metric_statistics, threshold):
        consecutive_high_points = 0
        all_metrics = []
        for point in metric_statistics['Datapoints']:
            if point[SUM] >= threshold:
                consecutive_high_points += 1
                print(f"consecutive_high_points: {consecutive_high_points} data_point: {point[SUM]}")
                all_metrics.append({
                    'StartTime': metric_statistics['StartTime'],
                    'EndTime': metric_statistics['EndTime'],
                    'Datapoint': point
                })
            else:
                print(f"consecutive_high_points: {consecutive_high_points} data_point: {point[SUM]}")
                consecutive_high_points = 0
                all_metrics = []

            if consecutive_high_points >= self.consecutive_points:
                return all_metrics, True
        return all_metrics, False

class AlarmTrigger:
    def __init__(self, config):
        self.config = config

    def trigger(self, all_metrics, metric_statistics, distribution_id, is_disable_triggered=False):
        alarm_manager = AlarmManager(self.config, metric_statistics)
        sum_str = ','.join(str(metric['Datapoint'][SUM]) for metric in all_metrics)
        print(f"sum list: {sum_str}")
        alarm = alarm_manager.create_alarm(metric_statistics['Datapoints'][-1], distribution_id, sum_str, self.config[THRESHOLD], self.config[CONSECUTIVE_POINTS], is_disable_triggered)
        self.send_notifications(alarm, is_disable_triggered)

    def triggerDisable(self, distribution_id, assumed_role_credentials):
        cf = CloudFrontManager(assumed_role_credentials)
        cf.disable_distribution(distribution_id)
    
    def send_notifications(self, alarm, is_disable_triggered):
        default_message = alarm.__dict__
        email_message = HelperUtils.convert_json_text(default_message)
        print(f"sns开关：{self.config[SEND_SNS_FLAG]}")
        if self.config[SEND_SNS_FLAG] == Status.OPEN.value:
            run_sns_operations(is_disable_triggered, self.config, self.config[PAYER_TOPIC_NAME], email_message)
        if SEND_LINKED_SNS_FLAG in self.config and self.config[SEND_LINKED_SNS_FLAG] == Status.OPEN.value:
            run_sns_operations(is_disable_triggered, self.config, self.config[LINKED_TOPIC_NAME], email_message)


class MetricManager:
    def __init__(self, account_configs):
        self.account_configs = account_configs
        self.sts = STSManager()

    def run(self):
        collector = DataCollector(self.account_configs)
        for distribution_id, metric_statistics, config, assumed_role_credentials in collector.collect_data():
            print(f"aws service id: {distribution_id}")
            evaluator = PointEvaluator(config)
            all_metrics, is_alarm_triggered = evaluator.evaluate(metric_statistics, config[THRESHOLD])
            print(f"is_alarm_triggered: {is_alarm_triggered}")
            if is_alarm_triggered:
                is_disable_triggered = evaluator.evaluate_for_disable(metric_statistics, config[AUTO_DISABLE_SERVICE_THRESHOLD])
                print(f"aws is_disable_triggered id: {is_disable_triggered}")
                trigger = AlarmTrigger(config)
                trigger.trigger(all_metrics, metric_statistics, distribution_id, is_disable_triggered)
                if is_disable_triggered:
                    trigger.triggerDisable(distribution_id, assumed_role_credentials)
