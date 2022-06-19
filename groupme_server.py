import base64
from flask import Flask, request
import requests
import os

# Non-private I think
GROUP_ID = 87556558

var = 'GROUPME_BOT_ID'
bot_id = os.getenv(var)
if not bot_id:
    raise Exception(f'Need to set {var}.')
# NOTE: for regular use, need to port-forward this from router to this machine
ip_var = 'MY_IP'
ip = os.getenv(ip_var)
if not ip:
    raise Exception(f'Need to set {ip_var}.')
server_var = 'DALLE_SERVER_ADDRESS'
server = os.getenv(server_var)
if not server:
    raise Exception(f'Need to set {server_var}.')
dalle_url = f'{server}/dalle'


APP = Flask(__name__)


def send_msg(bot_id, msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {'bot_id': bot_id, 'text': msg}
    res = requests.post(url, json=data)
    print(res.text)


def fetch_images(msg):
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


@APP.route("/message", methods=['POST'])
def on_message():
    print(request.json)
    message = request.json
    text = message['text']
    callword = '!dalle'
    if text.startswith(callword):
        fetch_images(text[len(callword):])
    return {'success': True}


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000)
    # TODO: put some length checking and stuff in there. Make all of the error messages really passive aggressive to specifically Tom
