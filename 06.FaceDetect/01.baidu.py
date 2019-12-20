import requests
import hashlib
from urllib import parse
import os
import base64
import time
import json


# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=RMA9la8lXIeV984v3TYgtQtp&client_secret=pHeA1Hf1ncpEWjry54dPqgNwNjGyQOHq'
response = requests.get(host)
if response:
    token = response.json()
    access_token = token['access_token']
    print(token['access_token'])

pic_path = r'F:/101.test/CelebA/Img/img_celeba.7z/img_celeba/img_celeba'

start = 0
end =200000

jsonfilename = 'tecent_result_'+time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())+'.json'

with open('configure.ini') as f:
    #print(f.readline())
    configure =str.split(f.readline(),',')
    print(configure)
    start = int(configure[0])
    end = int(configure[1])

for i in range(start,end):
    picname = '{:0>6d}'.format(i+1)+'.jpg'
    picfullpath = os.path.join(pic_path,picname)
    print(picfullpath)
    pic_base64=''
    with open(picfullpath,'rb') as f:
        pic_base64 = base64.b64encode(f.read())
        #print(pic_base64)
    if not pic_base64:
        continue

    url_face_faceshape = r'https://aip.baidubce.com/rest/2.0/face/v3/detect'
    while 1:
        params = {
            'image': pic_base64,
            'image_type': 'BASE64',
            'face_field': 'landmark',
            # 'sign': '',
        }

        headers = {"Content-Type":"application/json"}
        params_url = {"access_token":access_token}
        # print(params)

        try:
            request_face_faceshape = requests.post(url_face_faceshape, data=params, params=params_url, headers=headers)
            # request_face_faceshape = requests.post(url_face_faceshape,json=json.dumps(params))
            # print(request_face_faceshape.text)
            request_face_faceshape.raise_for_status()
        except requests.RequestException as e:
            print(e)
            continue

        face_faceshape_value = json.loads(request_face_faceshape.text, encoding='utf_8')
        #print(face_faceshape_value)
        qpsERROR=[4,17,18,19]
        if face_faceshape_value['error_code'] in qpsERROR:
            continue
        with open(jsonfilename,'a') as f:
            saveitem = json.dumps({picname:face_faceshape_value})
            print(saveitem)
            f.write(saveitem)
            f.write('\n')
        break




