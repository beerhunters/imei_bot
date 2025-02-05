# # # # Required Library
# # # from pprint import pprint
# # #
# # # import requests
# # #
# # # # Base URL
# # # url = "https://api.imeicheck.net/v1/services"
# # #
# # # token = "QPMgof1zgq5nDTIpO29jxI062Xx7cwz24kIN3pkO80cc54c8"
# # #
# # # # Add necessary headers
# # # headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
# # #
# # # # Execute request
# # # response = requests.get(url, headers=headers)
# # #
# # # pprint(response.text)
# # # Required Libraries
# # import requests
# # import json
# #
# # # Base URL
# # url = "https://api.imeicheck.net/v1/checks"
# #
# # token = "QPMgof1zgq5nDTIpO29jxI062Xx7cwz24kIN3pkO80cc54c8"
# #
# # # Add necessary headers
# # headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
# #
# # # Add body
# # body = json.dumps({"deviceId": "356735111052198", "serviceId": 1})
# #
# # # Execute request
# # response = requests.post(url, headers=headers, data=body)
# #
# # print(response.text)
# from pprint import pprint
#
# import requests
# import json
#
# url = "https://api.imeicheck.net/v1/services"
# token = "QPMgof1zgq5nDTIpO29jxI062Xx7cwz24kIN3pkO80cc54c8"
#
# payload = {}
# headers = {
#     "Authorization": "Bearer " + token,
#     "Accept-Language": "en",
#     "Content-Type": "application/json",
# }
#
# response = requests.request("GET", url, headers=headers, data=payload)
#
# pprint(response.text)
from pprint import pprint

import requests
import json

url = "https://api.imeicheck.net/v1/checks"

token = "QPMgof1zgq5nDTIpO29jxI062Xx7cwz24kIN3pkO80cc54c8"

payload = json.dumps({"deviceId": "356735111052198", "serviceId": 12})
headers = {
    "Authorization": "Bearer " + token,
    "Accept-Language": "en",
    "Content-Type": "application/json",
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint(response.text)
