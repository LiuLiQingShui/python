import os
import json
import pymongo
import threading
from flask import Flask,jsonify,request,abort
from werkzeug import security,utils
import CanBinDataProcessV3
import analyseData2
import GetDataFromServer
from flask import send_file,render_template,send_from_directory
from flask_cors import CORS
from flask_apscheduler import APScheduler
from apscheduler.triggers.interval import IntervalTrigger
import backupDatabase


import sys
if sys.executable.endswith("pythonw.exe"):
  sys.stdout = open(os.devnull, "w");
  sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
interval = IntervalTrigger(
        hours=6,  # 每天执行一次
        start_date='2019-4-20 09:00:00',
        end_date='2099-8-19 06:00:00',
        timezone='Asia/Shanghai')
scheduler.add_job(id='account_sync_job', func=backupDatabase.backupDatabase, trigger=interval)
scheduler.start()



CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

#UPLOAD_FOLDER = '/path/to/the/uploads'
UPLOAD_FOLDER = os.path.join(os.getcwd(),'bin')
ALLOWED_EXTENSIONS = set(['bin','dat'])
THREAD_COUNT = 1

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

class G:
    situ = []
    version = []


class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, DataFolder, filename,situ,version):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.DataFolder = DataFolder
        self.filename = filename
        self.situ = situ
        self.version = version
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        CanBinDataProcessV3.CanBinDataProcess(self.DataFolder, self.filename)
        analyseData2.analyseData(self.DataFolder, self.filename,self.situ,self.version)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/getsituiation',methods=['POST'])
def getsituiation():
    data = request.get_data()
    ##print(data)
    json_data = json.loads(data.decode("utf-8"))
    ##print(json_data)
    #print(json_data["situ"])
    #situ = json_data["situ"]
    G.situ = json_data["situ"]
    G.version = json_data["version"]
    return jsonify({"status": True})


@app.route('/missingwrong',methods=['POST'])
def missingwrong():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    saveMongoDBdict = json_data
    #print(saveMongoDBdict)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]
    mycol.insert_one(saveMongoDBdict)
    return jsonify({"status": True})


@app.route('/updateSituation',methods=['POST'])
def updateSituation():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    #print(json_data)
    ID = json_data['ID']
    Situation = json_data['Situation']
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]

    mycol_LDW = mydb["LDW"]
    myquery = {"OrangeBinData": ID+'.bin'}
    newvalues = {"$set": {"Situation": Situation}}
    mycol_LDW.update_many(myquery, newvalues)

    myquery = {"OrangeBinData": ID + '.dat'}
    mycol_LDW.update_many(myquery, newvalues)

    mycol_MissingWrong = mydb["MissingWrong"]
    myquery = {"ID": int(ID)}
    mycol_MissingWrong.update_many(myquery, newvalues)

    return jsonify({"status": True})


@app.route('/updateVersion',methods=['POST'])
def updateVersion():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    #print(json_data)
    ID = json_data['ID']
    version = json_data['version']
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]

    mycol_LDW = mydb["LDW"]
    myquery = {"OrangeBinData": ID+'.bin'}
    newvalues = {"$set": {"version": version}}
    mycol_LDW.update_many(myquery, newvalues)

    myquery = {"OrangeBinData": ID + '.dat'}
    mycol_LDW.update_many(myquery, newvalues)

    mycol_MissingWrong = mydb["MissingWrong"]
    myquery = {"ID": int(ID)}
    mycol_MissingWrong.update_many(myquery, newvalues)

    return jsonify({"status": True})

@app.route('/uploadTTC',methods=['POST'])
def uploadTTC():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    #print(json_data)
    GetDataFromServer.uploadTTC(json_data)
    return jsonify({"status": True})

@app.route('/delectTTC_manul',methods=['POST'])
def delectTTC_manul():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    #print(json_data)
    GetDataFromServer.delectTTC_manul(json_data)
    return jsonify({"status": True})


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # #print("AAAAAA")
    # #print(request.method)
    # if request.method == 'OPTIONS':
    #     #print("DDDDDDDDDDD")
    #     res = Flask.make_response()
    #     res.headers['Access-Control-Allow-Origin'] = '*'
    #     res.headers['Access-Control-Allow-Methods'] = 'POST，GET,OPTIONS'
    #     res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    #     return res
    if request.method == 'POST':
        for key in request.files.keys():
            file = request.files[key]
            if file and allowed_file(file.filename):
                filename = utils.secure_filename(file.filename)
                #print(filename)
                savefilepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(savefilepath)
                thread1 = myThread(THREAD_COUNT, app.config['UPLOAD_FOLDER'], filename,G.situ,G.version)
                thread1.start()
                thread_count = THREAD_COUNT + 1
                # CanBinDataProcessV2.CanBinDataProcess(app.config['UPLOAD_FOLDER'], filename)
        return 'succeed'
    return 'failed'


# @app.route('/',methods=['post'])
# def query():
#     if not request.json:
#         abort(400)
#     return jsonify({'task': tasks}),201
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')



@app.route('/')
def query():
    #return send_file("TestReport.html")
    return render_template("TestReportByVersion.html")


@app.route('/reportbytime')
def reportbytime():
    #return send_file("TestReport.html")
    #return render_template("TestReportByVersion.html")
    return render_template("TestReportByTime.html")

@app.route('/uploadbin')
def uploadbin():
    return render_template("uploadbin.html")

@app.route('/managerment')
def managerment():
    return render_template("EntryManagerment.html")

@app.route('/reportbyversion')
def reportbyversion():
    return render_template("TestReportByVersion.html")

@app.route('/getsummary',methods=['get'])
def getsummary():
    response = jsonify({'Summart': GetDataFromServer.getSummary()})
    # return jsonify({'Summart': GetDataFromServer.getSummary()}),200
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/getsummarymissingwrong',methods=['get'])
def getsummarymissingwrong():
    response = jsonify({'Summart': GetDataFromServer.getsummarymissingwrong()})
    # return jsonify({'Summart': GetDataFromServer.getSummary()}),200
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/getversion',methods=['get','POST'])
def getversion():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        type = json_data['Type']
        response = jsonify({'version': GetDataFromServer.getversion(type)})
        # return jsonify({'Summart': GetDataFromServer.getSummary()}),200
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/getOneItem',methods=['get', 'POST'])
def getOneItem():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        filename = json_data['filename']
        ##print({"Data": GetDataFromServer.getOneItem(filename)})
        response = jsonify({"Data": GetDataFromServer.getOneItem(str(filename))})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        #return jsonify({"Data": GetDataFromServer.getOneItem(filename)}),200


@app.route('/getOneItemmissingwrong',methods=['get', 'POST'])
def getOneItemmissingwrong():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        filename = json_data['ID']
        ##print({"Data": GetDataFromServer.getOneItemmissingwrong(filename)})
        response = jsonify({"Data": GetDataFromServer.getOneItemmissingwrong(filename)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        #return jsonify({"Data": GetDataFromServer.getOneItem(filename)}),200


@app.route('/deleteoneitem',methods=['get', 'POST'])
def deleteoneitem():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        filename = json_data['filename']
        ##print({"Data": GetDataFromServer.getOneItem(filename)})
        response = jsonify({"Data": GetDataFromServer.deleteoneitem(filename)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        #return jsonify({"Data": GetDataFromServer.getOneItem(filename)}),200


@app.route('/deleteoneitemmissingwrong',methods=['get', 'POST'])
def deleteoneitemmissingwrong():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        filename = json_data['ID']
        ##print({"Data": GetDataFromServer.getOneItem(filename)})
        response = jsonify({"Data": GetDataFromServer.deleteoneitemmissingwrong(filename)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        #return jsonify({"Data": GetDataFromServer.getOneItem(filename)}),200


@app.route('/getDataByTime',methods=['get', 'POST'])
def getDataByTime():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        starttime = json_data['starttime']
        endtime = json_data['endtime']
        Situation = json_data['Situation']
        #print(Situation)
        ##print({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime),Situation)})
        response = jsonify({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime),Situation)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
       # return jsonify({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime))}),200


@app.route('/getDataByTime_TTC_manul',methods=['get', 'POST'])
def getDataByTime_TTC_manul():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        starttime = json_data['starttime']
        endtime = json_data['endtime']
        Situation = json_data['Situation']
        #print(Situation)
        ##print({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime),Situation)})
        response = jsonify({"Data": GetDataFromServer.getDataByTime_TTC_manul(float(starttime),float(endtime),Situation)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response



@app.route('/getdatabyversion',methods=['get', 'POST'])
def getdatabyversion():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        version = json_data['version']
        Situation = json_data['Situation']
        #print(Situation)
        ##print({"Data": GetDataFromServer.getdatabyversion(version,Situation)})
        response = jsonify({"Data": GetDataFromServer.getdatabyversion(version,Situation)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
       # return jsonify({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime))}),200

@app.route('/getdatabyversionAll',methods=['get', 'POST'])
def getdatabyversionAll():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        #version = json_data['version']
        Situation = json_data['Situation']
        starttime = json_data['starttime']
        endtime = json_data['endtime']
        #print(Situation,starttime,endtime)
        ##print({"Data": GetDataFromServer.getdatabyversion(version,Situation)})
        response = jsonify({"Data": GetDataFromServer.getdatabyversionAll(Situation,starttime,endtime)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/getdatabyversionAll_TTC_manual',methods=['get', 'POST'])
def getdatabyversionAll_TTC_manual():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        #version = json_data['version']
        Situation = json_data['Situation']
        starttime = json_data['starttime']
        endtime = json_data['endtime']
        #print(Situation,starttime,endtime)
        ##print({"Data": GetDataFromServer.getdatabyversion(version,Situation)})
        response = jsonify({"Data": GetDataFromServer.getdatabyversionAll_TTC_manual(Situation,starttime,endtime)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/getdatabyversionmissingwrongAll',methods=['get', 'POST'])
def getdatabyversionmissingwrongAll():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        #version = json_data['version']
        Situation = json_data['Situation']
        starttime = json_data['starttime']
        endtime = json_data['endtime']
        #print(Situation,starttime,endtime)
        ##print({"Data": GetDataFromServer.getdatabyversion(version,Situation)})
        response = jsonify({"Data": GetDataFromServer.getdatabyversionmissingwrongAll(Situation,starttime,endtime)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/getDataByTimemissingwrong',methods=['get', 'POST'])
def getDataByTimemissingwrong():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        starttime = json_data['starttime']
        endtime = json_data['endtime']
        Situation = json_data['Situation']
        #print(Situation)
        ##print({"Data": GetDataFromServer.getDataByTimemissingwrong(float(starttime),float(endtime),Situation)})
        response = jsonify({"Data": GetDataFromServer.getDataByTimemissingwrong(float(starttime),float(endtime),Situation)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/getdatabyversionmissingwrong',methods=['get', 'POST'])
def getdatabyversionmissingwrong():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data:
        version = json_data['version']
        Situation = json_data['Situation']
        #print(Situation)
        ##print({"Data": GetDataFromServer.getdatabyversionmissingwrong(version,Situation)})
        response = jsonify({"Data": GetDataFromServer.getdatabyversionmissingwrong(version,Situation)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
       # return jsonify({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime))}),200


@app.route("/joinus",methods=['GET','POST'])
def index():
    data=request.get_json(force=True)
    if data:
        #print(data)
        return jsonify({"status": True})
    else:
        return jsonify({"status": False})


if __name__ =='__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=5000)
