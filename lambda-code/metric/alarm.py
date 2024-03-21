class Alarm:
    def __init__(self):
        self.name = "loghub request exception"
        self.description = ""
        self.state_change = "OK -> ALARM"
        self.reason_for_state_change = "Threshold Crossed: 1 out of the last 1 datapoints [75.36301625830178 (12/03/24 12:43:00)] was greater than the threshold (50.0) (minimum 1 datapoint for OK -> ALARM transition)."
        self.timestamp = None
        self.aws_account = None
        self.alarm_arn = None
        # self.datapoints = []

        self.threshold = {
            "metric_name": "Requests",
            "metric_namespace": "AWS/CloudFront",
            "dimensions": [
                {"Name": "Region", "Value": "Global"},
                {"Name": "DistributionId", "Value": "E3ERIBTA4YYF4P"}
            ],
            "period": 300,
            "extended_statistic": "p90",
            "unit": None,
            "treat_missing_data": "missing",
            "comparison_operator": "GreaterThanThreshold",
            "threshold": 50.0,
            "evaluation_total_periods": 1,
            "evaluation_periods": 1
        }

        self.state_change_actions = {
            "OK": [],
            "ALARM": ["arn:aws:sns:us-east-1:中文:alert-topic"],
            "INSUFFICIENT_DATA": []
        }

if __name__ == "__main__":
    print(Alarm().__dict__)