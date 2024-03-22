from alarm import Alarm
class AlarmManager:
    def __init__(self, config, metric_statistics):
        self.config = config
        self.metric_statistics = metric_statistics

    def create_alarm(self, point, distribution_id, sum_str, threshold, consecutive_high_points, is_disable_triggered):
        alarm = Alarm()
        alarm.name = (
            f"High request metrics for account: {self.config['account_id']}, "
            f"distribution id: {distribution_id},"
        )
        alarm.description = "请查看cloudfront分发监控，确认您的流量是否异常"

        # 假设 point['Timestamp'] 是一个 datetime 对象
        point_timestamp = point['Timestamp']
        # 获取毫秒部分
        milliseconds = point_timestamp.microsecond // 1000
        # 格式化日期和时间，包含毫秒
        formatted_datetime = point_timestamp.strftime("%Y%m%d%H%M%S") + f"{milliseconds:03d}"
        alarm.alarm_id = self.config['account_id'] + "-" + formatted_datetime
        alarm.aws_account = self.config['account_id']
        alarm.timestamp = point_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        alarm.state_change = "OK -> ALARM"
        alarm.reason_for_state_change = (
            f"连续{self.config['consecutive_points']}次在{self.config['period']/60}分钟时间段的总请求数列表为： {sum_str}，"
            f"均超过设定的阈值: {self.config['threshold']}. "
        )
        alarm.threshold = {
            "metric_name": self.metric_statistics['MetricName'],
            "metric_namespace": self.metric_statistics['Namespace'],
            "period": self.metric_statistics['Period'],
            "extended_statistic": "Sum",
            "unit": None,
            "threshold": threshold,
            "comparison_operator": "GreaterThanThreshold",
            "evaluation_periods": consecutive_high_points
        }
        alarm.state_change_actions = {
            "Action1": "采集指标",
            "Action2": "发送告警"
        }
        if is_disable_triggered:
            alarm.state_change_actions["Action3"] = "自动停止服务"

        return alarm
