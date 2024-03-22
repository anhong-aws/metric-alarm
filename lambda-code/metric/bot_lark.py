import requests
import json


import logging
logging.basicConfig(level=logging.INFO)
def send_lark_message(webhook_url, text_message):
    # 发送消息
    try:

        # 构造消息数据
        message = {
            "msgtype": "text",
            "text": {
                "content": text_message
            },
            "at": {
                "atMobiles": [],  # 被@人的手机号列表,可为空
                "isAtAll": False  # 是否@所有人,默认为False
            }
        }

        # 构建请求payload
        payload = {
            "msg_type": "text",
            "content": {
                "text": text_message
            }
        }

        # 将Python字典转换为JSON字符串
        message_json = json.dumps(payload)

        # 设置请求头
        headers = {
            "Content-Type": "application/json"
        }

        logging.info(f"Sending message to dingding")
        # 发送请求
        response = requests.post(webhook_url, data=message_json, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            logging.info("Message sent successfully")
        else:
            logging.info("消息发送失败，状态码:", response.status_code)
        # 打印响应结果
        # print(response.text)
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":

    # 替换为您的Lark机器人Webhook URL
    webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/07a77d6f-b71d-4ae3-b374-27d7e13f8697"
    send_lark_message(webhook_url, "这是一条测试消息")
