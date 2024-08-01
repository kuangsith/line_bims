import requests
import json
import config
from imgurpython import ImgurClient

url = config.url_broadcast

url_push = config.url_push

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


def send_broadcast(textmsg,imgurl):
    """
    Broadcast msg and img in one request
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
            },
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



def send_push(textmsg):
    """
    Sending push text msg, for testing only
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}",
        # "X-Line-Retry-Key":
    }

    payload = {
        "to": config.UID,  # Replace with the actual user ID
        "messages": [
            {
                "type": "text",
                "text": textmsg
            },
            {
                "type": "image",
                "originalContentUrl": "https://imgix.ranker.com/list_img_v2/505/3220505/original/3220505?fit=crop&fm=pjpg&q=80&dpr=2&w=1200&h=720",
                "previewImageUrl": "https://imgix.ranker.com/list_img_v2/505/3220505/original/3220505?fit=crop&fm=pjpg&q=80&dpr=2&w=1200&h=720"
            }
        ]
    }

    response = requests.post(url_push, headers=headers, data=json.dumps(payload))

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)