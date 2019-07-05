import requests

url = "https://eliotctl.fr/api/add/model/"

payload = "{\n    \"token\": \"ULTIMATE_TOKEN\",\n    \"address\": \"ECTWO-2EHK-MY4F-8BEH-DRXMQ\",\n    \"model\": {\n        \"vte\": \"fre\"\n    }\n}"
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