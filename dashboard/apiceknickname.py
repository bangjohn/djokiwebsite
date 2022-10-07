import requests

import requests
import json

import requests
nomorid = '12349273'
nomorserver = '2013'
url = "https://xcoinshop.com/api/v1/order/prepare/MOBILE_LEGENDS?code=MOBILE_LEGENDS&userId={nomorid}&zoneId={nomorserver}".format(nomorid=nomorid, nomorserver=nomorserver)

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)