import requests

from sender.static import BOT_TOKEN, CHAT_ID
from sender.utils import *


def send_message(msg):
    url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'.format(BOT_TOKEN, CHAT_ID, msg)
    requests.post(url)


def main():
    clear_screen()
    while True:
        msg = input('>> ')
        if msg == '--exit':
            uninstall_lib('telesend')
            break
        send_message(msg)


if __name__ == '__main__':
    main()
