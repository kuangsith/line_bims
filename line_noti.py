import requests
import json
import config
from imgurpython import ImgurClient

url = config.url

channel_access_token = config.token


def sendmsg(textmsg):
    """
    Sending text msg
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}",
        # "X-Line-Retry-Key":
    }

    payload = {
        # "to": config.UID,  # Replace with the actual user ID
        "messages": [
            {
                "type": "text",
                "text": textmsg
            }
        ]
    }


    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)


imgur_client = ImgurClient(config.imgur_cid, config.imgur_secret)

def upload_image_to_imgur(image_path):
    """Upload img to Imgur, preparation to send through line."""
    response = imgur_client.upload_from_path(image_path, anon=True)
    return response['link']


def sendimg(imgurl):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}",
        # "X-Line-Retry-Key":
    }

    payload = {
        # "to": config.UID,  # Replace with the actual user ID
        "messages": [
            {
                "type": "image",
                "originalContentUrl": imgurl,
                "previewImageUrl": imgurl
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
