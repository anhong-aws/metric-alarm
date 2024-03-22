import telegram
import logging
import asyncio
# TODO: 需要判断下chat_id是否存在
logging.basicConfig(level=logging.INFO)
async def send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE):
    # 发送消息
    try:
        logging.info(f"Sending message to chat ID: {CHAT_ID}")
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=MESSAGE)
        logging.info("Message sent successfully")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":

    # 替换为您自己的 Telegram Bot Token
    BOT_TOKEN = "7081516317:AAGje-aVGPswokFUL3Okxgz8efWLbBQjC7s"

    # 需要发送消息的用户或群组的 ID
    CHAT_ID = "-4194166355"

    # 要发送的消息内容
    MESSAGE = "测试：这是一条通过python发送的告警消息!"
    asyncio.run(send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE))
