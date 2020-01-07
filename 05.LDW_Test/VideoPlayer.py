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
playmode = 1
frameindex = 0
frameindex_div = 0
State_pasue = 0
fps = 0
play_Scale_value = 0
timenow = time.time()
image_background = Image.fromarray(cv2.cvtColor(cv2.imread(r'background.jpg'), cv2.COLOR_RGB2BGRA))
image_background = ImageTk.PhotoImage(image=image_background)
image_scale = Image.fromarray(cv2.cvtColor(cv2.imread(r'scale.png'), cv2.COLOR_RGB2BGRA))
image_scale = ImageTk.PhotoImage(image=image_scale)

thread_play = 0
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

class Backgroundopenfile (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        time.sleep(5)
        cap = cv2.VideoCapture(VideoPath)
        ret, frame = cap.read()
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        size = str(int(width)) + 'x' + str(int(height + 150))
        #window.geometry(size)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        videoRoi.configure(image=frame)
        videoRoi.image = frame
        cap.release()
        print("Exiting " + self.name)


def play():
    global VideoPath
    global frameindex
    global State_play
    global State_pasue
    global fps
    global frameindex_div
    global playmode
    global play_Scale_value
    #print(sys._getframe().f_lineno)
    cap = cv2.VideoCapture(VideoPath)
    print(VideoPath)
    if not cap.isOpened():
        Lock_StateChange.acquire()
        State_play = 0
        frameindex = 0
        State_pasue = 0
        Lock_StateChange.release()
        return
    Lock_StateChange.acquire()
    fps = cap.get(cv2.CAP_PROP_FPS)
    framecounts = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    framesectiontime = 1 / fps
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = str(int(width)) + 'x' + str(int(height + 200))
    #window.geometry(size)
    Lock_StateChange.release()
    pause = 0
    play = 0
    while True:
        Lock_StateChange.acquire()
        pause = State_pasue
        #print(pause)
        play = State_play
        playmodenow = playmode
        Lock_StateChange.release()
        if not play:
            Lock_StateChange.acquire()
            frameindex = 0
            State_pasue = 0
            Lock_StateChange.release()
            cap.release()
            btn_back1s.configure(state=tkinter.NORMAL)
            btn_forwards.configure(state=tkinter.NORMAL)
            btn_back_1_frame.configure(state=tkinter.NORMAL)
            btn_forwards_1_frame.configure(state=tkinter.NORMAL)
            btn_Skiptoframe.configure(state=tkinter.NORMAL)
            btn_playVideo.configure(state=tkinter.NORMAL)
            btn_playVideo_narmalspeed.configure(state=tkinter.NORMAL)
            information.configure(text=str(0))  # 该函数可能阻塞或异常退出。所以要放在锁的外部
            play_Scale.set(0)
            #window.title('VideoPlayer (LLQS)')
            cap = cv2.VideoCapture(VideoPath)
            ret, frame = cap.read()
            if ret:
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                size = str(int(width)) + 'x' + str(int(height + 200))
                #window.geometry(size)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(image=frame)
                videoRoi.configure(image=frame)
                videoRoi.image = frame
            else:
                global image_background
                videoRoi.configure(image=image_background)
                videoRoi.image = image_background
                information.configure(text=str(''))
                #window.geometry('640x600')
            cap.release()
            break
        if pause:
            Lock_StateChange.acquire()
            if frameindex_div!=0:
                frameindex = frameindex+frameindex_div-1
                frameindex_div = 0
                if frameindex<0:
                    frameindex = 0
                if frameindex>cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    frameindex = cap.get(cv2.CAP_PROP_FRAME_COUNT)-1
                cap.set(cv2.CAP_PROP_POS_FRAMES,frameindex)
                Lock_StateChange.release()
            elif not (play_Scale_value >= round(frameindex / framecounts * 100)-2 and play_Scale_value <= round(frameindex / framecounts * 100)+2):
                 print(play_Scale_value,frameindex,framecounts,round(frameindex / framecounts * 100))
                 frameindex = int(play_Scale_value/100*framecounts)
                 cap.set(cv2.CAP_PROP_POS_FRAMES,frameindex)
                 Lock_StateChange.release()
            else:
                Lock_StateChange.release()
                continue
        #print(sys._getframe().f_lineno)
        frametimestart = time.time()
        ret, frame = cap.read()
        if not ret:
            Lock_StateChange.acquire()
            #State_play = 0
            #frameindex = 0
            #State_pasue = 0
            State_pasue = 1
            Lock_StateChange.release()
            btn_back1s.configure(state=tkinter.NORMAL)
            btn_forwards.configure(state=tkinter.NORMAL)
            btn_back_1_frame.configure(state=tkinter.NORMAL)
            btn_forwards_1_frame.configure(state=tkinter.NORMAL)
            btn_Skiptoframe.configure(state=tkinter.NORMAL)
            btn_playVideo.configure(state=tkinter.NORMAL)
            btn_playVideo_narmalspeed.configure(state=tkinter.NORMAL)
            print('end')
            continue
            #break
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        videoRoi.configure(image=frame)
        videoRoi.image = frame
        frametimeend = time.time()
        waittime = round((framesectiontime-(frametimeend-frametimestart))*1000)
        if waittime>0 and playmodenow!=0:
            cv2.waitKey(waittime)
            print(waittime,frametimeend,frametimestart)
        else:
            cv2.waitKey(1)
        #print(sys._getframe().f_lineno)
        Lock_StateChange.acquire()
        text_frameindex = frameindex
        frameindex = frameindex + 1
        Lock_StateChange.release()
        information.configure(text=str(text_frameindex))#该函数可能阻塞或异常退出。所以要放在锁的外部
        #play_Scale_value
        play_Scale_value = round(text_frameindex / framecounts * 100)
        play_Scale.set(round(text_frameindex/framecounts*100))






def tk_selectVideoPath(event):
    path_ = filedialog.askopenfilename()
    print(path_)
    global VideoPath
    VideoPath = path_
    tk_VideoPath.set(path_)
    tk_stop(event)
    cap = cv2.VideoCapture(VideoPath)
    ret, frame = cap.read()
    if ret:
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        size = str(int(width)) + 'x' + str(int(height + 200))
        #window.geometry(size)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)
        videoRoi.configure(image=frame)
        videoRoi.image = frame
    cap.release()
    print(VideoPath)
    videoname = VideoPath.split('/')[-1]
    window.title(videoname)
    #thread2 = Backgroundopenfile(2, "Thread-Backgroundopenfile", 2)
    #thread2.start()
    #tk_playVideo(event)




def tk_playVideo_narmalspeed(event):
    playandpause(1)

def tk_playVideo(event):
    playandpause(0)

def playandpause(mode):
    global State_play
    global State_pasue
    global playmode
    # print(sys._getframe().f_lineno)
    if Lock_StateChange.acquire(1):
        play = State_play
        playmode = mode
        Lock_StateChange.release()
    else:
        return
    if not play:
        Lock_StateChange.acquire()
        State_play = 1
        if mode==2:
            State_pasue = 1
        Lock_StateChange.release()
        global thread_play
        thread_play = myThread(1, "Thread-1", 1)
        thread_play.start()
        if mode!=2:
            btn_back1s.configure(state=tkinter.DISABLED)
            btn_forwards.configure(state=tkinter.DISABLED)
            btn_back_1_frame.configure(state=tkinter.DISABLED)
            btn_forwards_1_frame.configure(state=tkinter.DISABLED)
            btn_Skiptoframe.configure(state=tkinter.DISABLED)

        if mode==1:
            btn_playVideo.configure(state=tkinter.DISABLED)
        elif mode==0:
            btn_playVideo_narmalspeed.configure(state=tkinter.DISABLED)
    else:
        Lock_StateChange.acquire()
        State_pasue = not State_pasue
        Btn_state = State_pasue
        print('Pause' if State_pasue else 'Play')
        Lock_StateChange.release()
        if Btn_state:
            btn_back1s.configure(state=tkinter.NORMAL)
            btn_forwards.configure(state=tkinter.NORMAL)
            btn_back_1_frame.configure(state=tkinter.NORMAL)
            btn_forwards_1_frame.configure(state=tkinter.NORMAL)
            btn_Skiptoframe.configure(state=tkinter.NORMAL)
            if mode == 1:
                btn_playVideo.configure(state=tkinter.NORMAL)
            elif mode == 0:
                btn_playVideo_narmalspeed.configure(state=tkinter.NORMAL)
        else:
            btn_back1s.configure(state=tkinter.DISABLED)
            btn_forwards.configure(state=tkinter.DISABLED)
            btn_back_1_frame.configure(state=tkinter.DISABLED)
            btn_forwards_1_frame.configure(state=tkinter.DISABLED)
            btn_Skiptoframe.configure(state=tkinter.DISABLED)
            if mode == 1:
                btn_playVideo.configure(state=tkinter.DISABLED)
            elif mode == 0:
                btn_playVideo_narmalspeed.configure(state=tkinter.DISABLED)

def tk_stop(event):
    global State_play
    Lock_StateChange.acquire()
    State_play = 0
    Lock_StateChange.release()
    pass

def tk_back1s(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_StateChange.acquire()
    frameindex_div = 0 - fps
    Lock_StateChange.release()

def tk_forward1s(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_StateChange.acquire()
    frameindex_div = 0 + fps
    Lock_StateChange.release()


def tk_back_1_frame(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_StateChange.acquire()
    frameindex_div =  -1
    Lock_StateChange.release()

def tk_forwards_1_frame(event):
    global frameindex
    global fps
    global frameindex_div
    Lock_StateChange.acquire()
    frameindex_div = 1
    Lock_StateChange.release()

def tk_Skiptoframe(event):
    index = int(Entry_Skiptoframe.get())
    global frameindex
    global frameindex_div
    Lock_StateChange.acquire()
    frameindex_div = index - frameindex+1
    Lock_StateChange.release()

    global State_play
    global State_pasue
    global playmode
    # print(sys._getframe().f_lineno)
    if Lock_StateChange.acquire(1):
        play = State_play
        Lock_StateChange.release()
    else:
        return
    if not play:
        Lock_StateChange.acquire()
        State_play = 1
        State_pasue = 1
        Lock_StateChange.release()
        global thread_play
        thread_play = myThread(1, "Thread-1", 1)
        thread_play.start()

def tk_play_Scale(event):
    global State_play
    global State_pasue
    global playmode
    global play_Scale_value
    # print(sys._getframe().f_lineno)
    if Lock_StateChange.acquire(1):
        play = State_play
        play_Scale_value = play_Scale.get()
        print(play_Scale_value)
        Lock_StateChange.release()
    else:
        return
    if not play:
        Lock_StateChange.acquire()
        State_play = 1
        State_pasue = 1
        Lock_StateChange.release()
        global thread_play
        thread_play = myThread(1, "Thread-1", 1)
        thread_play.start()



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



Lock_StateChange = threading.Lock()



window.title('VideoPlayer (LLQS)')
#window.geometry('640x600')
window.resizable(0,0)

#视频窗口
videoRoi = tkinter.Label(window)
videoRoi.grid(row=9,column=0,columnspan=12)
videoRoi.configure(image=image_background)

scaleRoi = tkinter.Label(window)
scaleRoi.grid(row=10,column=0,columnspan=12)
scaleRoi.configure(image=image_scale)


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
#播放、暂停键.normal
btn_playVideo_narmalspeed = tkinter.Button(window,text='Play/Pause')
btn_playVideo_narmalspeed.bind('<Button-1>',tk_playVideo_narmalspeed)
btn_playVideo_narmalspeed.grid(row=5,column=0,sticky='w')
#播放、暂停键.quick
btn_playVideo = tkinter.Button(window,text='Play/Pause (fast mode)')
btn_playVideo.bind('<Button-1>',tk_playVideo)
btn_playVideo.grid(row=5,column=1,sticky='w')
#停止键
btn_stop = tkinter.Button(window,text='Stop')
btn_stop.bind('<Button-1>',tk_stop)
btn_stop.grid(row=5,column=2,sticky='w')
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
#播放进度条
play_Scale = tkinter.Scale(window, from_=0, to=100, length=640, orient=tkinter.HORIZONTAL,command=tk_play_Scale)
play_Scale.grid(row=8,columnspan=12)

btn = tkinter.Button(window, text='key')
btn.bind_all('<KeyPress>', eventhandler)



window.mainloop()

