import os
import random
import requests

# Non-private I think
GROUP_ID = 87556558

var = 'GROUPME_BOT_TOKEN'
ip_var = 'MY_IP'
token = os.getenv(var)
if not token:
    raise Exception(f'Need to set {var}.')
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
    print(res.status_code, res.text)

    res_data = res.json()
    return res_data['response']['bot']['bot_id']


if __name__ == '__main__':
    bot_id = add_bot(GROUP_ID, token)
    print('MADE BOT WITH ID', bot_id)
    os.environ['GROUPME_BOT_ID'] = bot_id
    with open('bot_log.log', 'w+') as out:
        out.write(bot_id)
