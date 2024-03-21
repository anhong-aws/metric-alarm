from sns_operations import check_topic_existence, publish_message_to_topic
from constants import *

def run_sns_operations(is_disable_triggered, config, topic_name=None, message=None):
    if not topic_name:
        print("Please provide a topic name.")
        return
    
    topic_arn = check_topic_existence(topic_name)
    
    # 发布消息到主题
    if message:
        subject = 'AWS告警：CDN请求数量异常'
        type = 'alarm'
        if "use_mock" in config and config['use_mock'] == True:
            subject = "测试邮件：" + subject
            type = 'test'
        if is_disable_triggered == True:
            subject = "AWS告警：CDN请求数量异常自动停止CDN"
        publish_message_to_topic(topic_arn, subject, message, message, type)
    else:
        print("No message provided.")

