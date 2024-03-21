# cloudwatch.py
import datetime
import boto3
def get_metric_statistics(credentials, distribution, minutes = 30, period = 300, Statistics = 'Sum'):
    start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=minutes)
    end_time = datetime.datetime.now(datetime.timezone.utc)
    return get_metric_statistics_custom(credentials, distribution, start_time, end_time, period, Statistics)

def get_metric_statistics_custom(credentials, distribution, start_time, end_time, period = 300, Statistics = 'Sum'):

    metric_statistics = get_common_metric_statistics(credentials, distribution, start_time, end_time, period = 300, Statistics = 'Sum')
    if metric_statistics.get('Datapoints') and len(metric_statistics['Datapoints']) > 0:
        
        return {
            'StartTime': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'EndTime': end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'Datapoints': metric_statistics.get('Datapoints'),
            'MetricName': 'Requests',
            'Namespace': 'AWS/CloudFront',
            'Statistics': Statistics,
            'Period': period
        }
    else:
        return {
            'StartTime': start_time,
            'EndTime': end_time,
            'Datapoints': []
        }

def get_common_metric_statistics(credentials, distribution, start_time, end_time, period = 300, Statistics = 'Sum'):
    cloudwatch = boto3.client('cloudwatch',
                              aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'],
                              region_name='us-east-1')

    distribution_id = distribution['Id']
    time_range_minutes = (end_time - start_time).total_seconds() / 60
    num_data_points = time_range_minutes / (period / 60)
    if (num_data_points > 1440):
        print("开始时间:", start_time.strftime("%Y-%m-%d %H:%M:%S"))
        print("结束时间:", end_time.strftime("%Y-%m-%d %H:%M:%S"))
        print(f'exceeds the limit of 1440, time_range_minutes: {time_range_minutes} num_data_points: {num_data_points}')
        return
    metric_statistics = cloudwatch.get_metric_statistics(
        MetricName='Requests',
        Namespace='AWS/CloudFront',
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Sum'],
        Dimensions=[{'Name': 'DistributionId', 'Value': distribution_id},
                    {'Name': 'Region', 'Value': 'Global'}]
    )
    return metric_statistics
