import os
import requests


class FetchError(Exception):
    pass

var = 'DALLE_SERVER_ADDRESS'
server = os.getenv(var)
if not server:
    raise FetchError(f'No env variable {var}.')
url = f'{server}/dalle'

print(f'Requesting from {url}')
request = {
    'num_images': 5,
    'text': 'a large dog named Mason'
}
print(f'Sending {request}')
res = requests.post(url, json=request)
print(res.status_code)
images = res.json()
print(images)

import base64
for i, image in enumerate(images):
    with open(f'image_{i}.png', 'wb') as fh:
        fh.write(base64.b64decode(image))
