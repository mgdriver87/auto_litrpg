import base64
import requests
import json

key_imgbb = "3464b41a94a3e6a84c9c77924a9882b7"
res = ''

def upload_image(image_filename):
    upload_filename = image_filename
    upload_filename = '-'.join(upload_filename.split("\\")[-2:])
    with open(image_filename, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": key_imgbb,
            "image": base64.b64encode(file.read()),
            "name": upload_filename,
        }
        res = requests.post(url, payload)
        data = res.text
    data = json.loads(data)
    print(data)
    return data["data"]["url"]