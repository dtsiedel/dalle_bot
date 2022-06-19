import random
import requests
import os

# Non-private I think
GROUP_ID = 87556558

var = 'GROUPME_BOT_TOKEN'
ip_var = 'MY_IP'
token = os.getenv(var)
if not token:
    raise Exception(f'Need to set {var}.')
# TODO: for regular use, need to port-forward this from router to this machine
ip = os.getenv(ip_var)
if not ip:
    raise Exception(f'Need to set {ip_var}.')


number = random.randint(0, 10000000)
def add_bot(group, token, port=8000):
    url = f'https://api.groupme.com/v3/bots'

    data = {
        'bot': {
            'name': f'dalle_bot_{number}',
            'group_id': str(group),
            'callback_url': f'http://{ip}:{port}/message'
        }
    }
    print(url)
    print(data)
    res = requests.post(url, json=data, params={'token': token})
    print(res.status_code)

    res_data = res.json()
    return res_data['response']['bot']['bot_id']


def send_msg(bot_id, msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {'bot_id': bot_id, 'text': 'Hello world2'}
    res = requests.post(url, json=data)
    print(res.text)


# TODO: split add_bot and server stuff. For real use will only have one bot
# TODO: add_bot should set log the ID, and set it in an env variable that the server checks
if __name__ == '__main__':
    #bot_id = add_bot(GROUP_ID, token)
