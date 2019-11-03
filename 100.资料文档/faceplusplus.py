import requests
import hashlib
from urllib import parse
import os
import base64
import time
import json



pic_path = r'F:/101.test/CelebA/Img/img_celeba.7z/img_celeba/img_celeba'

start = 0
end =200000

jsonfilename = 'faceplusplus_result_'+time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())+'.json'

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
    if not pic_base64:
        continue
    #print(pic_base64)
    url_face_faceshape = r'https://api-cn.faceplusplus.com/facepp/v3/detect'
    while 1:
        params = {
            'api_key':'wF9uh2YgL1f4VrUbOFpdmqNjrxGz76h5',
            'api_secret':'MVQP8m9-jx2PETHSvdT4EiMkH28gji1B',
            'image_base64': pic_base64,
            'return_landmark': 2,
            'return_attributes': 'gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus',

        }
        try:
            request_face_faceshape = requests.post(url_face_faceshape, data=params)
            request_face_faceshape.raise_for_status()
        except requests.RequestException as e:
            print(e)
            print('error')
            break

        face_faceshape_value = json.loads(request_face_faceshape.text, encoding='utf_8')

        qpsERROR='CONCURRENCY_LIMIT_EXCEEDED'
        if 'error_message' in face_faceshape_value:
            if  qpsERROR in face_faceshape_value['error_message']:
                continue
        with open(jsonfilename,'a') as f:
            saveitem = json.dumps({picname:face_faceshape_value})
            print(saveitem)
            f.write(saveitem)
            f.write('\n')
        break




