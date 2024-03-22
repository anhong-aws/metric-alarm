import requests
import json


import logging
logging.basicConfig(level=logging.INFO)
def send_dingding_message(webhook_url, text_message):
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

        # 将Python字典转换为JSON字符串
        message_json = json.dumps(message)

        # 设置请求头
        headers = {
            "Content-Type": "application/json"
        }

        logging.info(f"Sending message to dingding")
        # 发送请求
        response = requests.post(webhook_url, data=message_json, headers=headers)
        # 检查响应状态码
        if response.status_code == 200 and response.json()['errcode']==0:
            logging.info("Message sent successfully")
        else:
            logging.info("消息发送失败，状态码:", response.status_code)
            # 打印响应结果
            logging.info(response.text)
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":

    # 钉钉机器人的Webhook地址
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=cf34c5039b75c5883a3271bcfb0979312a911242d560891f1c346b85d7a26abf"
    send_dingding_message(webhook_url, "alarm:这是一条测试消息")