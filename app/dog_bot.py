import os

import time
import logging

import telegram
import requests
import re

from telegram.error import NetworkError, Unauthorized
from dotenv import load_dotenv
load_dotenv()

update_id = None

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def bop(bot, update):
    # url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(os.getenv('TELEGRAM_API'))
    
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    messages = ['manda dogs', '/doguinho']
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            print(update.message.text)
            if update.message.text in {'/acende@Papocobot','/acende'}:
                print('NAO SOLTA ROJAO AIN AIN AIN AIN')
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='AIIINNNNNN'
                )
                time.sleep(0.5)
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='AUUUU AAAIN AINNN'
                )
                time.sleep(0.5)
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='ainn ainn'
                )
            if any( re.findall('|'.join(messages), str(update.message.text).lower() ) ) :
                bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=get_image_url()
                )

if __name__ == '__main__':
    main()