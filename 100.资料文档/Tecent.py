import hashlib
from urllib import parse
import os
import base64
import time
import requests
import json

def getReqSign(params,appkey):
    params1={}
    for item in sorted(params.keys()):
        #if params[item]:
        params1[item] = params[item]
    params1['app_key'] = appkey
    keyvaluestr = parse.urlencode(params1)
    #print(keyvaluestr)
    m2 = hashlib.md5()
    m2.update(keyvaluestr.encode("utf8"))
    return str.upper(m2.hexdigest())

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
    #print(picfullpath)
    pic_base64=''
    with open(picfullpath,'rb') as f:
        pic_base64 = base64.b64encode(f.read())
        #print(pic_base64)
    if not pic_base64:
        continue

    while 1:
        params = {
            'app_id': 2123477286,
            'image': pic_base64,
            'mode': 0,
            'time_stamp': int(time.time()),
            'nonce_str': 'jimutest',
            # 'sign': '',
        }
        appkey = 'GFQMBELJ4sAA8IYc'
        params['sign'] = getReqSign(params, appkey)
        # print(params['sign'])

        url_face_faceshape = r'https://api.ai.qq.com/fcgi-bin/face/face_faceshape'
        # print(params)

        try:
            request_face_faceshape = requests.post(url_face_faceshape, data=params)
            request_face_faceshape.raise_for_status()
            # request_face_faceshape = requests.post(url_face_faceshape,json=json.dumps(params))
            # print(request_face_faceshape.text)
        except requests.RequestException as e:
            print(e)
            continue


        face_faceshape_value = json.loads(request_face_faceshape.text, encoding='utf_8')
        #print(face_faceshape_value)
        if face_faceshape_value['ret']==9:
            continue
        with open(jsonfilename,'a') as f:
            saveitem = json.dumps({picname:face_faceshape_value})
            print(saveitem)
            f.write(saveitem)
            f.write('\n')
        break





