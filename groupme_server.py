import base64
from flask import Flask, request
import requests
import os

# Non-private I think
GROUP_ID = 42846333

var = 'GROUPME_BOT_ID'
bot_id = os.getenv(var)
if not bot_id:
    raise Exception(f'Need to set {var}.')
# NOTE: for regular use, need to port-forward this from router to this machine
ip_var = 'MY_IP'
ip = os.getenv(ip_var)
if not ip:
    raise Exception(f'Need to set {ip_var}.')
token_var = 'GROUPME_BOT_TOKEN'
token = os.getenv(token_var)
if not token:
    raise Exception(f'Need to set {token_var}.')
server_var = 'DALLE_SERVER_ADDRESS'
server = os.getenv(server_var)
if not server:
    raise Exception(f'Need to set {server_var}.')
dalle_url = f'{server}/dalle'


APP = Flask(__name__)


def send_msg(msg, image_url=None):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {'bot_id': bot_id, 'text': f'{msg}. Beep boop.'}
    if image_url:
        data['picture_url'] = image_url
    print(f'Sending {data} to {url}')
    res = requests.post(url, json=data)
    print(res.text)


def register_image(local_path):
    image_url = 'https://image.groupme.com/pictures'
    with open(local_path, 'rb') as image_binary:
        res = requests.post(image_url, data=image_binary, params={'token':token})
        print(res.status_code, res.text)
    return res.json()['payload']['url']


def fetch_images(msg, requester):
    print(f'Requesting from {dalle_url}')
    request = {
        'num_images': 1,
        'text': msg
    }
    print(f'Sending {request}')
    res = requests.post(dalle_url, json=request)
    print(res.status_code)
    images = res.json()

    image = images[0]
    with open(f'image.png', 'wb') as fh:
        fh.write(base64.b64decode(image))

    url = register_image('image.png')
    print('uploaded result to', url)

    send_msg(f'{msg}, requested by {requester}', url)


@APP.route("/message", methods=['POST'])
def on_message():
    print(request.json)
    message = request.json
    text = message['text']
    if len(text) > 200:
        send_msg('Text too long. Stop trying to break it, Tom (presumably).')
    else:
        callword = '!dalle'
        requester = message['name']
        if text.startswith(callword):
            fetch_images(text[len(callword):], requester)
    return {'success': True}


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000)
    # TODO: put some length checking and stuff in there. Make all of the error messages really passive aggressive to specifically Tom
