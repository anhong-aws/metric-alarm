import boto3

def create_topic(topic_name):
    sns_client = boto3.client('sns')
    response = sns_client.create_topic(Name=topic_name)
    return response['TopicArn']

def subscribe_email_to_topic(topic_arn, email_address):
    sns_client = boto3.client('sns')
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email_address
    )
    return response['SubscriptionArn']

def publish_message_to_topic(topic_arn, message):
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
