import json

import boto3
import yaml
from warrant.aws_srp import AWSSRP
import requests
from yaml import load

yfile = "config/config.yaml"
with open(yfile) as f:
    auth = yaml.load(f, Loader=yaml.SafeLoader)
client = boto3.client(auth["idp-host"], region_name=auth["region_name"])
aws = AWSSRP(username=auth["username"], password=auth["password"], pool_id=auth["pool_id"], client_id=auth["client_id"],
             client=client)
tokens = aws.authenticate_user()
# print(tokens)
with open("json/headers.json") as h:
    headers=json.loads(h.read())
# headers = json.loads(open("json/headers.json","r").read())
headers["authorization"] = tokens['AuthenticationResult']['AccessToken']
# response = requests.get(
#     'https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/apheleia/user',
#     headers=headers)
# print(response.json())
with open("json/user-audit.json") as h:
    payload=json.loads(h.read())
print(payload)
print(headers)
url='https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/apheleia/user-audit'
print(url)
print(requests.post(url,headers=headers,json=payload).text)
jd=json.loads("""{"filter":{"tenantIds":["TNTG_JcAiNzE5f6aAju"]},"project":{"avataarId":1,"name":1,"reqConfig":1}}""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/apheleia/tenant/search', headers=headers,
                    json=jd).status_code)
jd=json.loads("""{"isPublic":true}""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/experiences/unique-categories/TNTG_JcAiNzE5f6aAju', headers=headers,json=jd).status_code)
jd=json.loads("""{"isPublic":false}""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/experiences/unique-categories/TNTG_JcAiNzE5f6aAju', headers=headers,json=jd).status_code)
jd=json.loads("""{"isPublic":true,"categories":[],"pagination":{"limit":60,"page":1}}""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/experiences/search/TNTG_JcAiNzE5f6aAju', headers=headers,
                    json=jd).status_code)
jd=json.loads("""[{"key":"TNT_Xq6yVeUW66KU94/experiences/EXP_gCaim5DAasLGNYpNkYsFPcv3T/thumbnail.png","reqType":"GET"}]""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/apollo/signed-urls', headers=headers,
                    json=jd).status_code)
print(requests.get('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/apollo/web-view/TNTG_JcAiNzE5f6aAju/navs', headers=headers).status_code)
jd=json.loads("""[{"key":"TNT_Xq6yVeUW66KU94/experiences/EXP_gCaim5DAasLGNYpNkYsFPcv3T/thumbnail.png","reqType":"GET"}]""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/apollo/signed-urls', headers=headers,
                    json=jd).status_code)
jd=json.loads("""{"config":"https://apollo-qa-assets-us-east-1.s3.us-east-1.amazonaws.com/TNT_jN2angn7TQ67hW/experiences/EXP_ER2TPYw9BRYbZzDNtwgrxarUE/config.json","thumbnail":"https://apollo-qa-assets-us-east-1.s3.us-east-1.amazonaws.com/TNT_jN2angn7TQ67hW/experiences/EXP_ER2TPYw9BRYbZzDNtwgrxarUE/thumbnail.png","category":"Others"}""")
print(requests.patch('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/experiences/update/TNTG_JcAiNzE5f6aAju/EXP_zfv4VMVH6RPkWqcse4rWSUZq2', headers=headers,
                    json=jd).status_code)
jd=json.loads("""{"filters":{"types":["LME_MESH_RENDERER","BYO3D"]},"pagination":{"page":1,"limit":100}}""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/editor-records/search/TNTG_JcAiNzE5f6aAju', headers=headers,
                    json=jd).status_code)
jd=json.loads("""{"filters":{"types":["IMPLICIT"]},"pagination":{"page":1,"limit":100}}""")
print(requests.post('https://oc9rczvetg.execute-api.us-east-1.amazonaws.com/qa/editor-records/search/TNTG_JcAiNzE5f6aAju', headers=headers,
                    json=jd).status_code)
