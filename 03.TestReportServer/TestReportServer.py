import os
import threading
from flask import Flask,jsonify,request,abort
from werkzeug import security,utils
import CanBinDataProcessV2
import analyseData2
import GetDataFromServer



app = Flask(__name__)

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
ALLOWED_EXTENSIONS = set(['bin'])
THREAD_COUNT = 1

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, DataFolder, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.DataFolder = DataFolder
        self.filename = filename
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        CanBinDataProcessV2.CanBinDataProcess(self.DataFolder, self.filename)
        analyseData2.analyseData(self.DataFolder, self.filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = utils.secure_filename(file.filename)
            savefilepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(savefilepath)
            thread1 = myThread(THREAD_COUNT, app.config['UPLOAD_FOLDER'], filename)
            thread1.start()
            thread_count = THREAD_COUNT+1
            #CanBinDataProcessV2.CanBinDataProcess(app.config['UPLOAD_FOLDER'], filename)
            return 'succeed'
    return 'failed'

@app.route('/',methods=['post'])
def query():
    if not request.json:
        abort(400)
    return jsonify({'task': tasks}),201

@app.route('/getsummary',methods=['get'])
def getsummary():
    return jsonify({'Summart': GetDataFromServer.getSummary()}),200

@app.route('/getOneItem',methods=['get'])
def getOneItem():
    print(request.args)
    if request.args:
        filename = request.args.get('filename')
        print({filename: GetDataFromServer.getOneItem(filename)})
        return jsonify({filename: GetDataFromServer.getOneItem(filename)}),200

@app.route('/getDataByTime',methods=['get'])
def getDataByTime():
    print(request.args)
    if request.args:
        starttime = request.args.get('starttime')
        endtime = request.args.get('endtime')
        print({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime))})
        return jsonify({"Data": GetDataFromServer.getDataByTime(float(starttime),float(endtime))}),200

if __name__ =='__main__':
    app.run(debug=True)
