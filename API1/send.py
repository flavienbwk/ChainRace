import requests
import json

url = "https://eliotctl.fr/api/add/model/"
model = json.dumps({
    "action_space": [
        {
            "steering_angle": -30,
            "speed": 3.5,
            "index": 0
        },
        {
            "steering_angle": -30,
            "speed": 7,
            "index": 1
        },
        {
            "steering_angle": -15,
            "speed": 3.5,
            "index": 2
        },
        {
            "steering_angle": -15,
            "speed": 7,
            "index": 3
        },
        {
            "steering_angle": 0,
            "speed": 3.5,
            "index": 4
        },
        {
            "steering_angle": 0,
            "speed": 7,
            "index": 5
        },
        {
            "steering_angle": 15,
            "speed": 3.5,
            "index": 6
        },
        {
            "steering_angle": 15,
            "speed": 7,
            "index": 7
        },
        {
            "steering_angle": 30,
            "speed": 3.5,
            "index": 8
        },
        {
            "steering_angle": 30,
            "speed": 7,
            "index": 9
        }
    ]
}
)

payload = "{\n    \"token\": \"ULTIMATE_TOKEN\",\n    \"address\": \"ECTWO-2EHK-MY4F-8BEH-DRXMQ\",\n    \"model\": " + model + "\n}"
headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "/",
    'Cache-Control': "no-cache",
    'Host': "eliotctl.fr",
    'accept-encoding': "gzip, deflate",
    'content-length': "120",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)