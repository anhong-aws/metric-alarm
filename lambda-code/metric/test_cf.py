import pytest
import boto3
from moto import mock_aws
from cloud_front_manager import CloudFrontManager
from sts_manager import STSManager
from account_config_manager import AccountConfigManager

# @pytest.mark.sts
# def test_get_assumed_role_credentials():
#     # List all CloudFront distributions
#     cf = CloudFrontManager(assumed_role_credentials)
#     distributions = cf.list_deployed_distributions()
    


@pytest.mark.cf_mock
@mock_aws
def test_cf():
    # Mock the assume_role call
    with mock_aws():
        ac = AccountConfigManager()
        account_configs = ac.read_account_configs(use_mock=True)
        sts = STSManager()
        for config in account_configs:
            print(f"AccountId {config['account_id']} {config['account_name']}")
            assumed_role_credentials = sts.get_assumed_role_credentials(config["account_id"], config["role"])

            # List all CloudFront distributions
            cf = CloudFrontManager(assumed_role_credentials)
            
            cloudfront_client = boto3.client(
                'cloudfront',
                aws_access_key_id=assumed_role_credentials['AccessKeyId'],
                aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],
                aws_session_token=assumed_role_credentials['SessionToken']
            )

            # 定义分发配置
            distribution = {
                'CallerReference': 'my-distribution',  # 唯一的调用者引用
                'Comment': 'My CloudFront Distribution',  # 分发的描述
                'Enabled': True,  # 启用分发
                'Origins': {  # 您的源信息
                    'Quantity': 1,  # 源的数量
                    'Items': [{
                        'Id': 'myS3Origin',  # 源ID
                        'DomainName': 'mybucket.s3.amazonaws.com',  # 您的S3桶域名
                        'S3OriginConfig': {
                            'OriginAccessIdentity': ''  # 可选，如果使用OAI则填写
                        },
                    }]
                },
                'DefaultCacheBehavior': {  # 默认缓存行为
                    'TargetOriginId': 'myS3Origin',
                    'ViewerProtocolPolicy': 'allow-all',
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0
                    },
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {
                            'Forward': 'none'
                        },
                        'Headers': {
                            'Quantity': 0
                        }
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 86400,
                    'MaxTTL': 31536000,
                },
                'Aliases': {
                    'Quantity': 0  # 别名的数量
                }
            }

            # 创建分发
            response = cloudfront_client.create_distribution(DistributionConfig=distribution)

            # 打印分发的ID和域名
            print(response['Distribution']['Id'])
            print(response['Distribution']['DomainName'])
            # cf.disable_distribution(distribution_id=response['Distribution']['Id'])
            distributions = cf.list_deployed_distributions()
            # print(distributions)
            for distribution in distributions:
                print(f"{distribution['Id']}")
                cf.disable_distribution(distribution_id=distribution['Id'])