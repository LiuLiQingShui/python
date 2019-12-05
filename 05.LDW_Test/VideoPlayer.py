import tkinter
from tkinter import filedialog
import cv2
import PIL
from PIL import Image,ImageTk
import threading
import time
import sys

window = tkinter.Tk()

VideoPath=''
State_play = 0
frameindex = 0
frameindex_div = 0
State_pasue = 0
fps = 0
timenow = time.time()
image_background = Image.fromarray(cv2.cvtColor(cv2.imread(r'background.jpg'), cv2.COLOR_RGB2BGRA))
image_background = ImageTk.PhotoImage(image=image_background)
#image_background.show()
#print(image_background)
#cv2.imshow('back',cv2.imread(r'background.jpg'))

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        play()
        print("Exiting " + self.name)


def play():
    global VideoPath
    global frameindex
    global State_play
    global State_pasue
    global fps
    global frameindex_div
    #print(sys._getframe().f_lineno)
    cap = cv2.VideoCapture(VideoPath)
    Lock_State_stop.acquire()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = str(int(width))+'x'+str(int(height+150))
    window.geometry(size)
    Lock_State_stop.release()
    if not cap.isOpened():
        Lock_State_stop.acquire()
        State_play = 0
        frameindex = 0
        Lock_State_stop.release()

        Lock_State_pasue.acquire()
        State_pasue = 0
        Lock_State_pasue.release()
        return
    pause = 0
    play = 0
    #print(sys._getframe().f_lineno)
    while True:
        #print(sys._getframe().f_lineno)
        Lock_State_pasue.acquire()
        #print(sys._getframe().f_lineno)
        pause = State_pasue
        Lock_State_pasue.release()
        Lock_State_stop.acquire()
        play = State_play
        Lock_State_stop.release()
        #print(sys._getframe().f_lineno)
        #print('play',not play)
        if not play:
            Lock_State_pasue.acquire()
            frameindex = 0
            State_pasue = 0
            Lock_State_pasue.release()
            global image_background
            videoRoi.configure(image=image_background)
            videoRoi.image = image_background
            information.configure(text=str(''))
            window.geometry('640x550')
            break
        if pause:
            Lock_State_stop.acquire()
            if frameindex_div!=0:
                frameindex = frameindex+frameindex_div-1
                frameindex_div = 0
                if frameindex<0:
                    frameindex = 0
                if frameindex>cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    frameindex = cap.get(cv2.CAP_PROP_FRAME_COUNT)-1
                cap.set(cv2.CAP_PROP_POS_FRAMES,frameindex)
                Lock_State_stop.release()
            else:
                Lock_State_stop.release()
                continue
        #print(sys._getframe().f_lineno)
        ret, frame = cap.read()
        if not ret:
            Lock_State_stop.acquire()
            State_play = 0
            frameindex = 0
            Lock_State_stop.release()
            Lock_State_pasue.acquire()
            State_pasue = 0
            Lock_State_pasue.release()
            print('end')
            break
        #print(sys._getframe().f_lineno)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        videoRoi.configure(image=frame)
        videoRoi.image = frame
        cv2.waitKey(1)
        #print(sys._getframe().f_lineno)
        Lock_State_stop.acquire()
        print(sys._getframe().f_lineno)
        information.configure(text=str(frameindex))
        frameindex = frameindex + 1
        Lock_State_stop.release()
        print(sys._getframe().f_lineno)




def tk_selectVideoPath(event):
    path_ = filedialog.askopenfilename()
    print(path_)
    global VideoPath
    VideoPath = path_
    tk_VideoPath.set(path_)

def tk_playVideo(event):
    global State_play
    global State_pasue
    print(sys._getframe().f_lineno)
    if Lock_State_stop.acquire(1):
        print(sys._getframe().f_lineno)
        play = State_play
        Lock_State_stop.release()
    else:
        print(sys._getframe().f_lineno)
        return
    print(sys._getframe().f_lineno)
    if not play:
        Lock_State_stop.acquire()
        State_play = 1
        Lock_State_stop.release()
        thread1 = myThread(1, "Thread-1", 1)
        thread1.start()
    else:
        print(sys._getframe().f_lineno)
        Lock_State_pasue.acquire()
        print(sys._getframe().f_lineno)
        State_pasue = ~State_pasue
        Lock_State_pasue.release()
        print(sys._getframe().f_lineno)
        print('stop')

def tk_stop(event):
    global State_play
    Lock_State_stop.acquire()
    State_play = 0
    Lock_State_stop.release()
    pass

def tk_back1s(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_State_stop.acquire()
    frameindex_div = 0 - fps
    Lock_State_stop.release()

def tk_forward1s(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_State_stop.acquire()
    frameindex_div = 0 + fps
    Lock_State_stop.release()


def tk_back_1_frame(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_State_stop.acquire()
    frameindex_div =  -1
    Lock_State_stop.release()

def tk_forwards_1_frame(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_State_stop.acquire()
    frameindex_div = 1
    Lock_State_stop.release()

def tk_Skiptoframe(event):
    index = int(Entry_Skiptoframe.get())
    global frameindex
    global frameindex_div
    Lock_State_stop.acquire()
    frameindex_div = index - frameindex+1
    Lock_State_stop.release()
    pass

def eventhandler(event):
    global timenow
    if event.keysym == 'Left':
        tk_back1s(event)
    elif event.keysym == 'Right':
        tk_forward1s(event)
    elif event.keysym =='Up':
        tk_back_1_frame(event)
    elif event.keysym=='Down':
        tk_forwards_1_frame(event)
    elif event.keysym=='space':
        #timenow = time.time()
        tk_playVideo(event)
        #if time.time()-1>=timenow:



Lock_State_pasue = threading.Lock()
Lock_State_stop = threading.Lock()


window.title('VideoPlayer (LLQS)')
window.geometry('640x550')
window.resizable(0,0)

#视频窗口
videoRoi = tkinter.Label(window)
videoRoi.grid(row=0,column=0,columnspan=12)
videoRoi.configure(image=image_background)
#信息展示栏
information = tkinter.Label(window,justify = 'left',anchor = 'w')
information.grid(row=1,column=0,columnspan=12)
information.configure(text='information')
#选择视频路径
btn_selectVideo = tkinter.Button(window,text = 'Select video')
btn_selectVideo.bind("<Button-1>", tk_selectVideoPath)
btn_selectVideo.grid(row=4,column=0,sticky='W')
tk_VideoPath = tkinter.StringVar()
Entry_selectVideo = tkinter.Entry(window,textvariable = tk_VideoPath,width=60).grid(row=4,column=1,columnspan=3,sticky='W')
#播放栏
#播放、暂停键
btn_playVideo = tkinter.Button(window,text='Play')
btn_playVideo.bind('<Button-1>',tk_playVideo)
btn_playVideo.grid(row=5,column=0,sticky='w')
#停止键
btn_stop = tkinter.Button(window,text='Stop')
btn_stop.bind('<Button-1>',tk_stop)
btn_stop.grid(row=5,column=1,sticky='w')
#后退1s键
btn_back1s = tkinter.Button(window,text='back 1s')
btn_back1s.bind('<Button-1>',tk_back1s)
btn_back1s.grid(row=6,column=0,sticky='w')
#前进1s键
btn_forwards = tkinter.Button(window,text='forward 1s')
btn_forwards.bind('<Button-1>',tk_forward1s)
btn_forwards.grid(row=6,column=1,sticky='w')
#后退1s帧
btn_back_1_frame = tkinter.Button(window,text='back 1 frame')
btn_back_1_frame.bind('<Button-1>',tk_back_1_frame)
btn_back_1_frame.grid(row=6,column=2,sticky='w')
#前进1s帧
btn_forwards_1_frame = tkinter.Button(window,text='forward 1 frame')
btn_forwards_1_frame.bind('<Button-1>',tk_forwards_1_frame)
btn_forwards_1_frame.grid(row=6,column=3,sticky='w')
#定位到某一帧
btn_Skiptoframe = tkinter.Button(window,text = 'Skip to frame')
btn_Skiptoframe.bind("<Button-1>", tk_Skiptoframe)
btn_Skiptoframe.grid(row=7,column=0,sticky='W')
tk_Skiptoframeindex = tkinter.StringVar()
Entry_Skiptoframe = tkinter.Entry(window,textvariable = tk_Skiptoframeindex)
Entry_Skiptoframe.grid(row=7,column=1,sticky='W')

btn = tkinter.Button(window, text='key')
btn.bind_all('<KeyPress>', eventhandler)



window.mainloop()

