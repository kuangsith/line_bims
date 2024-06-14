import requests
import json
import config

url = config.url

channel_access_token = config.token
def sendmsg(textmsg):
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
