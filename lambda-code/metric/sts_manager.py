import boto3

class STSManager:
    def __init__(self):
        """
        Initializes the STS manager.
        """
        self.sts_client = boto3.client('sts')
    
    def get_assumed_role_credentials(self, *args):
        if len(args) == 1:
            return self.get_assumed_role_credentials_by_arn(*args)
        elif len(args) == 2:
            return self.get_assumed_role_credentials_by_id(*args)
        else:
            raise ValueError("Invalid number of arguments.")
        
    def get_assumed_role_credentials_by_id(self, account_id, role):
        """
        Retrieves temporary session credentials using AWS STS (Security Token Service)
        based on account ID and role name.

        :param account_id: The AWS account ID.
        :param role: The name of the role to assume.
        :return: A dictionary containing temporary credentials.
        """
        assumed_role_arn = self.get_assumed_role_arn(account_id, role)
        print(assumed_role_arn)
        return self.get_assumed_role_credentials_by_arn(assumed_role_arn)
    
    def get_assumed_role_credentials_by_arn(self, role_arn):
        """
        Retrieves temporary session credentials using AWS STS (Security Token Service).

        :param role_arn: The Amazon Resource Name (ARN) of the role to assume.
        :return: A dictionary containing temporary credentials.
        """
        try:
            assumed_role_object = self.sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName='AssumeRoleSession1'
            )
            return {
                'AccessKeyId': assumed_role_object['Credentials']['AccessKeyId'],
                'SecretAccessKey': assumed_role_object['Credentials']['SecretAccessKey'],
                'SessionToken': assumed_role_object['Credentials']['SessionToken']
            }
        except Exception as e:
            print(f"Error assuming role {role_arn}: {e}")
            return None
    
    def get_assumed_role_arn(self, account_id, role):
        assume_role_arn = f'arn:aws:iam::{account_id}:role/{role}'
        return assume_role_arn
