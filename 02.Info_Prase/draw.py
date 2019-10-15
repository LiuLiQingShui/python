import csv
from pathlib import Path
import os
import re
import time
import numpy as np
import matplotlib
import pylab as pl
import warnings
import pandas as pd


#根据ID选择数据。RadarSelect.csv为对应的ID和帧范围
def selectRadarData(DataFolder,h):
    TestCasefile = os.path.join(DataFolder, h + '_RadarSelect.csv')
    RadarDatafile = os.path.join(DataFolder, h + '_ROBJ.csv')
    with open(TestCasefile) as f:
        reader = csv.reader(f)
        content = list(reader)
        dict=[]
        dataStart = 0
        for row in content:
            if row[0]=='START':
                dataStart = 1
                continue
            if row[0] == 'END':
                dataStart = 0
                break
            if dataStart:
                dict.append(row)
        if (len(dict))<3:
            print(TestCasefile+" is empty")
            return
        with open(RadarDatafile) as f_radar:
            reader_radar = csv.reader(f_radar)
            content_radar = list(reader_radar)
            RadarData=[]
            for row_radar in content_radar:
                row_radar_frameID = int(row_radar[1])
                row_radar_obj_num = int(row_radar[4])
                allrange_low = int(dict[2][0])
                allrange_high = int(dict[len(dict)-1][1])
                if row_radar_frameID<allrange_low:
                    continue
                if row_radar_frameID>allrange_high:
                    break
                for slectrange in range(2,len(dict)):
                    slectrange_low = int(dict[slectrange][0])
                    slectrange_high = int(dict[slectrange][1])
                    obi_id = int(dict[slectrange][2])
                    if row_radar_frameID>=slectrange_low and row_radar_frameID<=slectrange_high:
                        findlaber11 = 0
                        for k_row_radar in range(len(row_radar)):
                            if "obj_id_ID_" in row_radar[k_row_radar]:
                                if int(row_radar[k_row_radar + 1]) == obi_id:
                                    row_radar_obi_id_obj_x = int(row_radar[k_row_radar + 9])
                                    row_radar_obi_id_obj_y = int(row_radar[k_row_radar + 11])
                                    row_radar_obi_id_obj_Vy = int(row_radar[k_row_radar + 21])
                                    findlaber11 = 1
                                    RadarData.append(
                                        [row_radar_frameID, obi_id, row_radar_obi_id_obj_x, row_radar_obi_id_obj_y,row_radar_obi_id_obj_Vy/3.6])
                                    break
                        if findlaber11==0:
                            1
                        break
    RadarData_csv = RadarData
    return RadarData_csv

def selectJimuData(DataFolder,h):
    TestCasefile = os.path.join(DataFolder, h + '_JimuSelect.csv')
    JimuDatafile = os.path.join(DataFolder, h + '_OBJS.csv')
    with open(TestCasefile) as f:
        reader = csv.reader(f)
        content = list(reader)
        dict=[]
        dataStart = 0
        for row in content:
            if row[0]=='START':
                dataStart = 1
                continue
            if row[0] == 'END':
                dataStart = 0
                break
            if dataStart:
                dict.append(row)
        if (len(dict))<3:
            print(TestCasefile+" is empty")
            return
        with open(JimuDatafile) as f_radar:
            reader_radar = csv.reader(f_radar)
            content_radar = list(reader_radar)
            RadarData=[]
            for row_radar in content_radar:
                row_radar_frameID = int(row_radar[1])
                row_radar_obj_num = int(row_radar[4])
                allrange_low = int(dict[2][0])
                allrange_high = int(dict[len(dict)-1][1])
                if row_radar_frameID<allrange_low:
                    continue
                if row_radar_frameID>allrange_high:
                    break

                for slectrange in range(2,len(dict)):
                    slectrange_low = int(dict[slectrange][0])
                    slectrange_high = int(dict[slectrange][1])
                    obi_id = int(dict[slectrange][2])
                    if row_radar_frameID>=slectrange_low and row_radar_frameID<=slectrange_high:
                        findlaber11 = 0
                        for k_row_radar in range(len(row_radar)):
                            if "objId_ID_" in row_radar[k_row_radar]:
                                if int(row_radar[k_row_radar + 1]) == obi_id:
                                    row_radar_obi_id_obj_x = float(row_radar[k_row_radar + 15])
                                    row_radar_obi_id_obj_y = float(row_radar[k_row_radar + 13])
                                    row_radar_obi_id_obj_Vy = float(row_radar[k_row_radar + 17])
                                    findlaber11 = 1
                                    RadarData.append(
                                        [row_radar_frameID, obi_id, row_radar_obi_id_obj_x, row_radar_obi_id_obj_y,row_radar_obi_id_obj_Vy])
                                    break
                        if findlaber11==0:
                            1
                        break
    RadarData_csv = RadarData
    return RadarData_csv


def getCDF(arrayinput,xticks):
    yticks = []
    for k in range(len(xticks)):
        yticks.append(arrayinput[np.where(arrayinput<=xticks[k])].size)
    return np.array(yticks)

def draw(DataFolder,h):
    if not (os.path.exists(os.path.join(DataFolder, h + '_JimuSelect.csv')) and os.path.exists(
            os.path.join(DataFolder, h + '_RadarSelect.csv'))):
        return
    jimudata = selectJimuData(DataFolder,h)
    radardata = selectRadarData(DataFolder,h)
    jimudata = np.array(jimudata)
    radardata = np.array(radardata)
    distance_min = 15
    distance_max = 180
    with open("distance.csv") as f:
        reader = csv.reader(f)
        content = list(reader)
        distance_min = int(content[0][0])
        distance_max = int(content[0][1])
        print('distance range',distance_min,distance_max)
    ratio = []
    cleanDataLT150=[]
    for k in range(len(jimudata)):
        for tt in range(len(radardata)):
            if jimudata[k][0] == radardata[tt][0]:
                if radardata[tt][0] > 0 and radardata[tt][3] > 0 :
                    ratio.append([jimudata[k][0], (jimudata[k][3] - radardata[tt][3] / 100) / (radardata[tt][3] / 100)*100])
                    if radardata[tt][3]<distance_max*100 and radardata[tt][3]>distance_min*100:
                        cleanDataLT150.append([jimudata[k][0], (jimudata[k][3] - radardata[tt][3] / 100) / (radardata[tt][3] / 100)* 100,jimudata[k][3],  radardata[tt][3] / 100,jimudata[k][4], radardata[tt][4],jimudata[k][2], radardata[tt][2]/100])
                break
    ratio = np.array(ratio)
    breakpoint_jimudata = []
    first = jimudata[0][0]
    endlaber = 0
    for k in range(1, len(jimudata)):
        next = jimudata[k][0]
        if abs(next - first) >= 2:
            breakpoint_jimudata.append(k - 1)
            if k == len(jimudata):
                endlaber = 1
        first = next
    if endlaber == 0:
        breakpoint_jimudata.append(len(jimudata) - 1)
    breakpoint_radar = []
    first = radardata[0][0]
    endlaber = 0
    for k in range(1, len(radardata)):
        next = radardata[k][0]
        if abs(next - first) >= 2:
            breakpoint_radar.append(k - 1)
            if k == len(radardata):
                endlaber = 1
        first = next
    if endlaber == 0:
        breakpoint_radar.append(len(radardata) - 1)
    breakpoint_ratio = []
    first = ratio[0][0]
    endlaber = 0
    for k in range(1, len(ratio)):
        next = ratio[k][0]
        if abs(next - first) >= 2:
            breakpoint_ratio.append(k - 1)
            if k == len(ratio):
                endlaber = 1
        first = next
    if endlaber == 0:
        breakpoint_ratio.append(len(ratio) - 1)
    pl.mpl.rcParams['font.sans-serif'] = ['SimHei']
    pl.rcParams['axes.unicode_minus'] = False
    first = 0
    for k in range(len(breakpoint_radar)):
        next = breakpoint_radar[k]
        if k==0:
            pl.plot(radardata[first:next, 0], radardata[first:next, 3] / 100, color="blue",label = "Radar")
        else:
            pl.plot(radardata[first:next, 0], radardata[first:next, 3] / 100, color="blue")
        first = breakpoint_radar[k] + 1
    first = 0
    for k in range(len(breakpoint_jimudata)):
        next = breakpoint_jimudata[k]
        if k==0:
            pl.plot(jimudata[first:next, 0], jimudata[first:next, 3], color="red",label = "Jimu")
        else:
            pl.plot(jimudata[first:next, 0], jimudata[first:next, 3], color="red")
        first = breakpoint_jimudata[k] + 1
    pl.grid()
    pl.xlabel('frame index')
    pl.ylabel('longitudinal distance/m')
    pl.legend()
    pl.ylim([distance_min, distance_max])
    pl.savefig(os.path.join(DataFolder, h + '_00.frame.png'))
    pl.close()
    np.savetxt(os.path.join(DataFolder, h + '_jimudata.csv'), jimudata, delimiter=',')
    np.savetxt(os.path.join(DataFolder, h + '_radardata.csv'), radardata, delimiter=',')
    np.savetxt(os.path.join(DataFolder, h + '_ratio.csv'), ratio, delimiter=',')
    np.savetxt(os.path.join(DataFolder, h + '_speed.csv'), cleanDataLT150, delimiter=',')
    SaveData = pd.DataFrame(cleanDataLT150,columns=['frame index','ratio','jimu distance y','radar distance y','jimu speed','radar speed','jimu distance x','radar distance x'])
    SaveData.to_csv(os.path.join(DataFolder, h + '_Data.csv'),encoding='utf_8_sig', index=False)
    np.savetxt(os.path.join(DataFolder, h + '_breakpoint_jimudata.csv'), ((np.array(jimudata[breakpoint_jimudata]))[:,0]+1)[:len(breakpoint_jimudata)-1], delimiter=',')
    np.savetxt(os.path.join(DataFolder, h + '_breakpoint_radar.csv'), ((np.array(radardata[breakpoint_radar]))[:,0]+1)[:len(breakpoint_radar)-1], delimiter=',')
    np.savetxt(os.path.join(DataFolder, h + '_breakpoint_ratio.csv'), ((np.array(ratio[breakpoint_ratio]))[:,0]+1)[:len(breakpoint_ratio)-1], delimiter=',')
    if len(cleanDataLT150)>0:
        grid1 = pl.GridSpec(1, 2, wspace=0.5, hspace=0.5)
        ax1 = pl.subplot(grid1[0, 0])
        ax2 = pl.subplot(grid1[0, 1])
        cleanDataLT180 = cleanDataLT150.copy()
        ttt = np.array(cleanDataLT150)[:,1]
        distance = np.array(cleanDataLT150)[:,3]
        jimudis = np.array(cleanDataLT150)[:,2]
        ratio = np.array(cleanDataLT150)[:,1]

        pl.sca(ax1)
        pl.hist(ttt, 100,  histtype='bar', facecolor='red', alpha=0.75)
        pl.xlabel('error/%')
        pl.title('PDF')
        cleanDataLT150 =abs( np.array(cleanDataLT150)[:,1])
        xticks = np.linspace(cleanDataLT150.min(),cleanDataLT150.max(),len(cleanDataLT150))
        print('xticks 1: ',xticks)
        yticks = getCDF(abs(cleanDataLT150), xticks)
        pl.sca(ax2)
        pl.plot(xticks,yticks/yticks[len(yticks)-1]*100,color='coral')
        pl.grid()
        pl.xlabel('error/%')
        pl.title('Empirical CDF')
        pl.xticks(np.linspace(0,max([(xticks.max()//5+1)*5,10]),5))
        pl.yticks(np.linspace(0,100,5))
        pl.xlim([0,max([(xticks.max()//5+1)*5,10])])
        pl.ylim([0, 100])
        pl.savefig(os.path.join(DataFolder, h + '_00.cdf_pdf.png'))
        pl.close()

        order = np.argsort(distance)
        distance = distance[order]
        jimudis = jimudis[order]
        ratio =ratio[order]
        pl.plot(distance,ratio)
        pl.grid()
        pl.plot([0,180],[5,5],color='crimson',linestyle='--')
        pl.plot([0, 180], [-5, -5],color='crimson',linestyle='--')
        pl.xlabel('distance/m')
        pl.ylabel('error/%')
        pl.xlim([0, 180])
        pl.savefig(os.path.join(DataFolder, h + '_00.distanceAnderror.png'))
        pl.close()

        if  os.path.exists(os.path.join(DataFolder, h + '_RadarSelect_Static.csv')):
            with open(os.path.join(DataFolder, h + '_RadarSelect_Static.csv')) as f:
                reader = csv.reader(f)
                content = list(reader)
                checkpoint = []
                distance = np.array(cleanDataLT180)[:, 3]
                jimudis = np.array(cleanDataLT180)[:, 2]
                ratio = np.array(cleanDataLT180)[:, 1]
                frame =  np.array(cleanDataLT180)[:, 0]
                for row in content:
                    frameStart = int(row[0])
                    frameEnd = int(row[1])
                    tempFrame = frame.copy()
                    for kk in np.where(frame<frameStart):
                        tempFrame[kk]=0
                    for kk in np.where(frame>frameEnd):
                        tempFrame[kk]=0
                    distance_step = distance[np.where(tempFrame>0 )]
                    jimu_step = jimudis[np.where(tempFrame>0 )]
                    checkpoint.append([np.mean(distance_step),np.mean(jimu_step),np.std(distance_step),np.std(jimu_step)])
                if len(checkpoint)>0:
                    checkpoint = np.array(checkpoint)
                    order = np.argsort(checkpoint[:,0])
                    distance = checkpoint[:,0][order]
                    jimudis = checkpoint[:,1][order]
                    ratio = (jimudis-distance)/distance*100
                    dis_var = checkpoint[:,2][order]
                    jimu_var = checkpoint[:,3][order]
                    pl.plot(np.arange(distance.size)+1, distance, color='blue',label = "Radar", marker='D' )
                    pl.plot(np.arange(distance.size) + 1, jimudis, color='red', label="Jimu", marker='o')
                    pl.xlabel('Test Step')
                    pl.ylabel('distance(average distance value in the step period)/m')
                    pl.legend()
                    pl.savefig(os.path.join(DataFolder, h + '_00.Static_distance.png'))
                    pl.close()
                    pl.plot(distance, dis_var, color='blue',label = "Radar", marker='D' )
                    pl.plot(distance, jimu_var, color='red', label="Jimu", marker='o')
                    pl.xlabel('distance/m')
                    pl.ylabel('standard 标准差')
                    pl.legend()
                    pl.savefig(os.path.join(DataFolder, h + '_00.Static_Standard.png'))
                    pl.close()
                    pl.plot(distance, (jimudis-distance)/distance*100, color='red',  marker='o' )
                    pl.xlabel('distance/m')
                    pl.ylabel('average error/%')
                    pl.legend()
                    pl.savefig(os.path.join(DataFolder, h + '_00.Static_averageErrorRatio.png'))
                    pl.close()






