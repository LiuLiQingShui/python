import bitstring
import struct
import time
import re
import os
import csv
from pathlib import Path


def TypeHeaderlist():
    return ['VINF','ADAS','LANE','OBJS','ROBJ','ICAN']

def prasePacket(TypeHeader,packet):
    Data = packet
    Result = []
    if TypeHeader == 'VINF':
        Result.append(["type",(struct.unpack_from("B",Data,0))[0]])
        Result.append(["format", (struct.unpack_from("B", Data, 1))[0]])
        Result.append(["reserved ", (struct.unpack_from("H", Data, 2))[0]])
        Result.append(["width", (struct.unpack_from("H", Data, 4))[0]])
        Result.append(["height", (struct.unpack_from("H", Data, 6))[0]])
        Result.append(["frame_index", (struct.unpack_from("I", Data, 8))[0]])
        Result.append(["timestamp", (struct.unpack_from("I", Data, 12))[0]])
        return Result
    if TypeHeader == 'ADAS':
        Result.append(["fcw_flag",(struct.unpack_from("B",Data,0))[0]])
        Result.append(["pdw_flag", (struct.unpack_from("B", Data, 1))[0]])
        Result.append(["tsr_flag", (struct.unpack_from("B", Data, 2))[0]])
        Result.append(["limit_flag", (struct.unpack_from("B", Data, 3))[0]])
        return Result
    if TypeHeader == 'LANE':
        Result.append(["state",(struct.unpack_from("B",Data,0))[0]])
        Result.append(["lane_num", (struct.unpack_from("B", Data, 1))[0]])
        Result.append(["reserved", (struct.unpack_from("H", Data, 2))[0]])
        for k in range((struct.unpack_from("B", Data, 1))[0]):
            Result.append(["lane_id"+"_ID_"+str(k), (struct.unpack_from("B", Data, 4+12*k))[0]])
            Result.append(["lane_exit" +"_ID_"+ str(k), (struct.unpack_from("B", Data, 5 + 12 * k))[0]])
            Result.append(["lane_type" +"_ID_"+ str(k), (struct.unpack_from("B", Data, 6 + 12 * k))[0]])
            Result.append(["lane_quality "+"_ID_" + str(k), (struct.unpack_from("B", Data, 7 + 12 * k))[0]])
            Result.append(["top_x"+"_ID_" + str(k), (struct.unpack_from("H", Data, 8 + 12 * k))[0]])
            Result.append(["top_y" +"_ID_"+ str(k), (struct.unpack_from("H", Data, 10 + 12 * k))[0]])
            Result.append(["bottom_x" +"_ID_"+ str(k), (struct.unpack_from("H", Data, 12 + 12 * k))[0]])
            Result.append(["bottom_y" +"_ID_"+ str(k), (struct.unpack_from("H", Data, 14 + 12 * k))[0]])
        return Result
    if TypeHeader == 'OBJS':
        Result.append(["obj_num", (struct.unpack_from("I", Data, 0))[0]])
        for k in range((struct.unpack_from("I", Data, 0))[0]):
            Result.append(["objId"+"_ID_"+str(k), (struct.unpack_from("i", Data, 4+116*k))[0]])
            Result.append(["label" + "_ID_" + str(k), (struct.unpack_from("i", Data, 8 + 116 * k))[0]])
            Result.append(["used3d" + "_ID_" + str(k), (struct.unpack_from("i", Data, 12 + 116 * k))[0]])
            Result.append(["center" + "_ID_" + str(k), (struct.unpack_from("i", Data, 16 + 116 * k))[0]])
            Result.append(["warn_flag" + "_ID_" + str(k), (struct.unpack_from("i", Data, 20 + 116 * k))[0]])
            Result.append(["prob" + "_ID_" + str(k), (struct.unpack_from("f", Data, 24 + 116 * k))[0]])
            Result.append(["v_dist" + "_ID_" + str(k), (struct.unpack_from("f", Data, 28 + 116 * k))[0]])
            Result.append(["h_dist" + "_ID_" + str(k), (struct.unpack_from("f", Data, 32 + 116 * k))[0]])
            Result.append(["v_speed" + "_ID_" + str(k), (struct.unpack_from("f", Data, 36 + 116 * k))[0]])
            Result.append(["h_speed" + "_ID_" + str(k), (struct.unpack_from("f", Data, 40 + 116 * k))[0]])
            Result.append(["width" + "_ID_" + str(k), (struct.unpack_from("f", Data, 44 + 116 * k))[0]])
            Result.append(["height" + "_ID_" + str(k), (struct.unpack_from("f", Data, 48 + 116 * k))[0]])
            Result.append(["warn_time" + "_ID_" + str(k), (struct.unpack_from("f", Data, 52 + 116 * k))[0]])
            Result.append(["box.x" + "_ID_" + str(k), (struct.unpack_from("i", Data, 56 + 116 * k))[0]])
            Result.append(["box.y" + "_ID_" + str(k), (struct.unpack_from("i", Data, 60 + 116 * k))[0]])
            Result.append(["box.width" + "_ID_" + str(k), (struct.unpack_from("i", Data, 64 + 116 * k))[0]])
            Result.append(["box.height" + "_ID_" + str(k), (struct.unpack_from("i", Data, 68 + 116 * k))[0]])
            Result.append(["rear.x" + "_ID_" + str(k), (struct.unpack_from("i", Data, 72 + 116 * k))[0]])
            Result.append(["rear.y" + "_ID_" + str(k), (struct.unpack_from("i", Data, 76 + 116 * k))[0]])
            Result.append(["rear.width" + "_ID_" + str(k), (struct.unpack_from("i", Data, 80 + 116 * k))[0]])
            Result.append(["rear.height" + "_ID_" + str(k), (struct.unpack_from("i", Data, 84 + 116 * k))[0]])
            Result.append(["side1.x" + "_ID_" + str(k), (struct.unpack_from("i", Data, 88 + 116 * k))[0]])
            Result.append(["side1.y" + "_ID_" + str(k), (struct.unpack_from("i", Data, 92 + 116 * k))[0]])
            Result.append(["side2.x" + "_ID_" + str(k), (struct.unpack_from("i", Data, 96 + 116 * k))[0]])
            Result.append(["side2.y" + "_ID_" + str(k), (struct.unpack_from("i", Data, 100 + 116 * k))[0]])
            Result.append(["side3.x" + "_ID_" + str(k), (struct.unpack_from("i", Data, 104 + 116 * k))[0]])
            Result.append(["side3.y" + "_ID_" + str(k), (struct.unpack_from("i", Data, 108 + 116 * k))[0]])
            Result.append(["side4.x" + "_ID_" + str(k), (struct.unpack_from("i", Data, 112 + 116 * k))[0]])
            Result.append(["side4.y" + "_ID_" + str(k), (struct.unpack_from("i", Data, 116 + 116 * k))[0]])
        return Result
    if TypeHeader == 'ROBJ':
        Result.append(["obj_num",(struct.unpack_from("I",Data,0))[0]])
        for k in range((struct.unpack_from("i", Data, 0))[0]):
            Result.append(["obj_id"+"_ID_"+str(k), (struct.unpack_from("B", Data, 4+16*k))[0]])
            Result.append(["radar_type" + "_ID_" + str(k), (struct.unpack_from("B", Data, 5 + 16 * k))[0]])
            Result.append(["obj_type" + "_ID_" + str(k), (struct.unpack_from("B", Data, 6 + 16 * k))[0]])
            Result.append(["obj_position" + "_ID_" + str(k), (struct.unpack_from("B", Data, 7 + 16 * k))[0]])
            Result.append(["obj_x" + "_ID_" + str(k), (struct.unpack_from("h", Data, 8 + 16 * k))[0]])
            Result.append(["obj_y" + "_ID_" + str(k), (struct.unpack_from("h", Data, 10 + 16 * k))[0]])
            Result.append(["obj_rcs" + "_ID_" + str(k), (struct.unpack_from("h", Data, 12+ 16 * k))[0]])
            Result.append(["obj_angle" + "_ID_" + str(k), (struct.unpack_from("h", Data, 14 + 16 * k))[0]])
            Result.append(["ttc_time" + "_ID_" + str(k), (struct.unpack_from("B", Data, 16 + 16 * k))[0]])
            Result.append(["hmw_time" + "_ID_" + str(k), (struct.unpack_from("B", Data, 17 + 16 * k))[0]])
            Result.append(["obj_y_vrel" + "_ID_" + str(k), (struct.unpack_from("h", Data, 18 + 16 * k))[0]])
        return Result
    if TypeHeader == 'ICAN':
        Result.append(["speed",(struct.unpack_from("i",Data,0))[0]])
        Result.append(["steering_angle", (struct.unpack_from("i", Data, 4))[0]])
        Result.append(["steering_speed", (struct.unpack_from("i", Data, 8))[0]])
        Result.append(["yaw_rate", (struct.unpack_from("i", Data, 12))[0]])
        Result.append(["brake", (struct.unpack_from("b", Data, 16))[0]])
        Result.append(["reverse", (struct.unpack_from("b", Data, 17))[0]])
        Result.append(["left_light", (struct.unpack_from("b", Data, 18))[0]])
        Result.append(["right_light", (struct.unpack_from("b", Data, 19))[0]])
        return Result
    return None


#解析info文件内的数据
def praseInfo(DataFolder,filename,h):
    UsbData_Path = os.path.join(DataFolder, filename)
    #print(UsbData_Path)
    print("Start Processing : ",UsbData_Path)
    testresult_csv_path = os.path.join(DataFolder, h + '_testresult_ALL.csv')
    testresult_txt_path = os.path.join(DataFolder, h + '_testresult_ALL.txt')
    with open(testresult_csv_path, 'w') as fw:
        1
    with open(testresult_txt_path, 'w') as fw:
        1
    for title in TypeHeaderlist():
        filepath = os.path.join(DataFolder, h + '_'+title+'.csv')
        with open(filepath, 'w') as fw:
            1
        filepath = os.path.join(DataFolder, h + '_' + title + '.txt')
        with open(filepath, 'w') as fw:
            1

    f = open(UsbData_Path, 'rb')
    data = 1
    frame_index = 1
    count = 0
    while data:
        data = f.read(4)
        try:
            #print((struct.unpack('4s', data))[0])
            TypeHeader = ((struct.unpack('4s', data))[0]).decode('ascii')
            #print(TypeHeader)
        except:
            #data = f.read(4)
            #print("Finish 1!")
            continue
        if TypeHeader not in TypeHeaderlist():
            continue
        data = f.read(4)
        try:
            DataSize = (struct.unpack('<L', data))[0]
        except:
            print("Finish 2!")
            break
        data = f.read(DataSize)
        try:
            result = prasePacket(TypeHeader,data)
            if TypeHeader=="VINF":
                frame_index=result[5][1]
                count = count + 1
        except:
            print("prasePacket failed!")
            break
        with open(testresult_txt_path, 'a') as fw:
            fw.write(str(count))
            fw.write("  ")
            fw.write(str(frame_index))
            fw.write("  ")
            fw.write(TypeHeader)
            fw.write("  ")
            for j in range(len(result)):
                fw.write(result[j][0])
                fw.write("  ")
                fw.write(str(result[j][1]))
                fw.write("  ")
            fw.write("\n")
        with open(testresult_csv_path, 'a') as fw:
            fw.write(str(count))
            fw.write(",")
            fw.write(str(frame_index))
            fw.write(",")
            fw.write(TypeHeader)
            fw.write(",")
            for j in range(len(result)):
                fw.write(result[j][0])
                fw.write(",")
                fw.write(str(result[j][1]))
                fw.write(",")
            fw.write("\n")
        filepath = os.path.join(DataFolder, h + '_'+TypeHeader+'.csv')
        with open(filepath, 'a') as fw:
            fw.write(str(count))
            fw.write(",")
            fw.write(str(frame_index))
            fw.write(",")
            fw.write(TypeHeader)
            fw.write(",")
            for j in range(len(result)):
                fw.write(result[j][0])
                fw.write(",")
                fw.write(str(result[j][1]))
                fw.write(",")
            fw.write("\n")
        filepath = os.path.join(DataFolder, h + '_' + TypeHeader + '.txt')
        with open(filepath, 'a') as fw:
            fw.write(str(count))
            fw.write("  ")
            fw.write(str(frame_index))
            fw.write("  ")
            fw.write(TypeHeader)
            fw.write("  ")
            for j in range(len(result)):
                fw.write(result[j][0])
                fw.write("  ")
                fw.write(str(result[j][1]))
                fw.write("  ")
            fw.write("\n")
    print("Process finished !")
    print("\n")




