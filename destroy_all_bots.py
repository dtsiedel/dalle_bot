import os
import requests

# Non-private I think
GROUP_ID = 42846333

var = 'GROUPME_BOT_TOKEN'
token = os.getenv(var)
if not token:
    raise Exception(f'Need to set {var}.')


def delete_bot(token, bot_id):
    print('delete', bot_id)
    url = f'https://api.groupme.com/v3/bots/destroy'
    data = {
        'bot_id': bot_id
    }
    delete = requests.post(url, json=data, params={'token': token})
    print(delete.status_code, delete.text)


def delete_bots(token):
    url = f'https://api.groupme.com/v3/bots'
    get = requests.get(url, params={'token': token})
    print('fetch list', get.status_code, get.text)
    results = get.json()
    lst = results['response']
    print(lst)

    for bot in lst:
        delete_bot(token, bot['bot_id'])


if __name__ == '__main__':
    inpt = input('Destroy all bots. Are you sure? (y/N): ')
    if inpt != 'y':
        print('ABORTING')
    else:
        delete_bots(token)
