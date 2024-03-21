import boto3

class CloudFrontManager:
    def __init__(self, credentials):
        """
        Initializes the CloudFront manager with AWS credentials.

        :param credentials: A dictionary containing AWS access key ID, secret access key, and session token.
        """
        self.cloudfront_client = boto3.client(
            'cloudfront',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    def list_deployed_distributions(self):
        """
        Lists deployed CloudFront distributions.

        :return: A list of deployed distribution details.
        """
        distributions = self.cloudfront_client.list_distributions()
        if 'DistributionList' in distributions and 'Items' in distributions['DistributionList']:
            return [d for d in distributions['DistributionList']['Items'] if d['Status'] == 'Deployed']
        else:
            return []

    def disable_distribution(self, distribution_id):
        """
        Disables a CloudFront distribution.

        :param distribution_id: The ID of the CloudFront distribution to disable.
        """
        try:
            config_response = self.cloudfront_client.get_distribution_config(Id=distribution_id)
            distribution_config = config_response['DistributionConfig']
            
            # 修改您需要更改的配置部分
            distribution_config['Enabled'] = False
            # 更新分发配置
            update_response = self.cloudfront_client.update_distribution(
                DistributionConfig=distribution_config,
                Id=distribution_id,
                IfMatch=config_response['ETag']  # 获取 ETag，它是必需的
            )
            print(f"Successfully disabled CloudFront distribution {distribution_id}")
            return update_response
        except Exception as e:
            print(f"Error disabling distribution {distribution_id}: {e}")
            return


