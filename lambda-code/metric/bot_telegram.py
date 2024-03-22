import requests
import json
import logging
logging.basicConfig(level=logging.INFO)

def send_telegram_message(webhook_url, chat_id, text_message):
    # 发送消息
    try:
        # 构建请求payload
        payload = {
            "chat_id": chat_id,
            "text": text_message
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

    # 替换为您的telegram机器人Webhook URL
    webhook_url = "https://api.telegram.org/bot7081516317:AAGje-aVGPswokFUL3Okxgz8efWLbBQjC7s/sendMessage"
    send_telegram_message(webhook_url,"-4194166355", "这是一条测试消息")

