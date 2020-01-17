import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def JimuVsRadar(DataFolder,filename,mode,breakpointexit,drawSpeed = False):
    print('-----------------------------------------------------------------------------')
    print('开始统计分析：' + os.path.join(DataFolder, filename) )

    pd.set_option('expand_frame_repr', False)
    pd.set_option("display.max_rows", 2000)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fileID = filename.split(r'.')[0]

    if not os.path.exists(os.path.join(DataFolder,fileID+'_OBJS.csv')):
        print('Error:' + os.path.join(DataFolder, filename) + '的障碍物信息数据不存在（_OBJS.csv），请检查')
        return
    if not os.path.exists(os.path.join(DataFolder,fileID+'_ID_Selected.csv')):
        print('Error:' + os.path.join(DataFolder, filename) + '_ID_Selected.csv文件不存在。请检查')
        return

    df_IDSelect =pd.read_csv(os.path.join(DataFolder,fileID+'_ID_Selected.csv'), encoding='utf_8_sig')
    StageName = df_IDSelect['static test'].dropna()
    df_IDSelect = df_IDSelect.drop(
        ['stats range', 'static test'], axis=1).astype(np.float)
    if len(StageName)!=len(df_IDSelect['static start frame']):
        Name = []
        for k in range(len(df_IDSelect['static start frame'])):
            Name.append('Stage '+str(k+1))
        StageName = pd.DataFrame({'Name':Name,
                                  'frameindex':df_IDSelect['static start frame']})
    else:
        StageName = pd.DataFrame({'Name': StageName,
                                  'frameindex': df_IDSelect['static start frame']})
    df_objs_Jimu = pd.read_csv(os.path.join(DataFolder,fileID+'_OBJS.csv'), encoding='utf_8_sig',
                               usecols=['frame_index', 'objId', 'v_dist', 'h_dist', 'v_speed', 'h_speed',
                                        'width', 'height']).astype(np.float)
    df_objs_Jimu[['frame_index']] = df_objs_Jimu[['frame_index']].fillna(method='pad')
    df_ID_Jimu = df_IDSelect[['Jimu object id', 'Jimu start frame', 'Jimu end frame']].dropna()
    if len(df_ID_Jimu) == 0:
        print('Error:' + os.path.join(DataFolder, filename) + '_ID_Selected.csv的Jimu ID内容填写错误或未填写，请检查')
        return
    df_Jimu = pd.DataFrame(columns=df_objs_Jimu.columns)
    for k in range(len(df_ID_Jimu)):
        df_Jimu_section_frameindex = df_objs_Jimu[
            (df_objs_Jimu['frame_index'] >= df_ID_Jimu.iloc[k]['Jimu start frame']) & (
                    df_objs_Jimu['frame_index'] <= df_ID_Jimu.iloc[k]['Jimu end frame'])][
            ['frame_index']].drop_duplicates('frame_index')
        df_Jimu_section = pd.merge(df_Jimu_section_frameindex, df_objs_Jimu[
            (df_objs_Jimu['objId'] == df_ID_Jimu.iloc[k]['Jimu object id']) & (
                    df_objs_Jimu['frame_index'] >= df_ID_Jimu.iloc[k]['Jimu start frame']) & (
                    df_objs_Jimu['frame_index'] <= df_ID_Jimu.iloc[k]['Jimu end frame'])], how='left',
                                   on='frame_index')
        # df_Jimu_section =  df_objs_Jimu[
        #     (df_objs_Jimu['objId'] == df_ID_Jimu.iloc[k]['Jimu object id']) & (
        #             df_objs_Jimu['frame_index'] >= df_ID_Jimu.iloc[k]['Jimu start frame']) & (
        #             df_objs_Jimu['frame_index'] <= df_ID_Jimu.iloc[k]['Jimu end frame'])]
        df_Jimu = pd.concat([df_Jimu, df_Jimu_section])
    if len(df_Jimu) == 0:
        print('Error:' + os.path.join(DataFolder, filename) + '的frame index与所填写的不一致，请检查')
        return
    df_Jimu.to_csv(os.path.join(DataFolder,fileID+'_JimuDetails.csv'),index=False,encoding='utf_8_sig')
    print('Jimu的详细距离数据信息保存至'+os.path.join(DataFolder,fileID+'_JimuDetails.csv'))
    if not os.path.exists(os.path.join(DataFolder,fileID+'_ROBJ.csv')):
        print('Error:' + os.path.join(DataFolder, filename) + '的雷达数据不存在（_ROBJ.csv），请检查')
        return
    df_objs_Radar = pd.read_csv(os.path.join(DataFolder,fileID+'_ROBJ.csv'), encoding='utf_8_sig',
                                usecols=['frame_index', 'obj_id', 'obj_x', 'obj_y','obj_x_vrel','obj_y_vrel']).astype(np.float)
    df_objs_Radar[['frame_index']] = df_objs_Radar[['frame_index']].fillna(method='pad')
    df_objs_Radar[['obj_x', 'obj_y']] = df_objs_Radar[['obj_x', 'obj_y']]
    df_ID_Radar = df_IDSelect[['Radar object id', 'Radar start frame', 'Radar end frame']].dropna()
    if len(df_ID_Radar)==0:
        print('Error:'+os.path.join(DataFolder,filename)+'_ID_Selected.csv的Radar ID内容填写错误或未填写，请检查')
        return
    df_Radar = pd.DataFrame(columns=df_objs_Radar.columns)
    for k in range(len(df_ID_Radar)):
        df_Radar_section_frameindex = df_objs_Radar[
            (df_objs_Radar['frame_index'] >= df_ID_Radar.iloc[k]['Radar start frame']) & (
                        df_objs_Radar['frame_index'] <= df_ID_Radar.iloc[k]['Radar end frame'])][
            ['frame_index']].drop_duplicates('frame_index')
        df_Radar_section = pd.merge(df_Radar_section_frameindex, df_objs_Radar[
            (df_objs_Radar['obj_id'] == df_ID_Radar.iloc[k]['Radar object id']) & (
                        df_objs_Radar['frame_index'] >= df_ID_Radar.iloc[k]['Radar start frame']) & (
                        df_objs_Radar['frame_index'] <= df_ID_Radar.iloc[k]['Radar end frame'])], how='left',
                                    on='frame_index')
        df_Radar = pd.concat([df_Radar, df_Radar_section])
    DistanceRange=np.array([15,180])
    temp = df_IDSelect['distance'].dropna().to_numpy()
    if len(temp)==2 and temp[0]<temp[1]:
        DistanceRange = temp
    else:
        print('Warning: 统计的最小、最大距离未设置，将使用默认的15~180m。如需统计其他范围请填写ID_Selected.csv中对应字段')
    print('Distance Range to analyse:', DistanceRange)
    Data_union = pd.merge(df_Jimu, df_Radar, how='outer', on='frame_index', suffixes=('_Jimu', '_Radar'))

    if breakpointexit<=0:
        Data_union = Data_union.dropna()

    Data_longtitudinalDistanceToFrameIndex = Data_union[['frame_index', 'h_dist', 'v_dist','obj_x', 'obj_y','v_speed', 'obj_y_vrel','h_speed', 'obj_x_vrel']].rename(
        columns={'frame_index': 'frame index', 'v_dist': 'Jimu', 'obj_y': 'Radar'})
    #print(Data_longtitudinalDistanceToFrameIndex)
    df = Data_longtitudinalDistanceToFrameIndex[
        (Data_longtitudinalDistanceToFrameIndex['Radar'] >= DistanceRange[0]) & (
                    Data_longtitudinalDistanceToFrameIndex['Radar'] <= DistanceRange[1])&(Data_longtitudinalDistanceToFrameIndex['Jimu'] > 0)]
    framestart = df.iloc[0]['frame index']
    frameend = df.iloc[-1]['frame index']
    print(framestart,frameend)
    Data_longtitudinalDistanceToFrameIndex = Data_longtitudinalDistanceToFrameIndex[
        (Data_longtitudinalDistanceToFrameIndex['frame index'] >= framestart) & (
                    Data_longtitudinalDistanceToFrameIndex['frame index'] <= frameend)].sort_values(by=['frame index'])
    print(Data_longtitudinalDistanceToFrameIndex)
    Data_longtitudinalDistanceToFrameIndex.plot(x='frame index', y=['Jimu', 'Radar'], style=['b', 'r'], kind='line')
    plt.grid()
    plt.xlabel(r'frame index')
    plt.ylabel(r'longitudinal distance / m')
    plt.title(r'Jimu与Radar纵向（Y）测距对比')
    plt.savefig(os.path.join(DataFolder,fileID+'_Distance_Y_01_OverView.png'))
    print('Jimu与Radar纵向（Y）测距对比图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_01_OverView.png'))

    Data_longtitudinalDistanceToFrameIndex.plot(x='frame index', y=['h_dist', 'obj_x'], style=['b', 'r'], kind='line')
    plt.grid()
    plt.legend(('Jimu', 'Radar'))
    plt.xlabel(r'frame index')
    plt.ylabel(r'Horizontal distance / m')
    plt.title(r'Jimu与Radar横向（X）测距对比')
    plt.savefig(os.path.join(DataFolder,fileID+'_Distance_X_01_OverView.png'))
    print('Jimu与Radar横向（X）测距对比图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_X_01_OverView.png'))

    if drawSpeed:
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        Data_longtitudinalDistanceToFrameIndex.plot(x='frame index', y=['v_speed', 'obj_y_vrel'], style=['b', 'r'], kind='line',ax=ax1)
        Data_longtitudinalDistanceToFrameIndex.plot(x='frame index', y=['Radar'], style=['k--'],
                                                    kind='line', ax=ax2)
        ax1.legend_.remove()
        ax1.set_xlabel(r'frame index')
        ax1.set_ylabel(r'纵向相对速度（Y）')
        ax1.legend(labels=('Jimu相对速度值', 'Radar相对速度值'),loc='upper left')
        ax1.grid()
        ax2.legend_.remove()
        ax2.set_xlabel(r'frame index')
        ax2.set_ylabel(r'从坐标：纵向距离')
        ax2.legend(labels=(r'纵向距离（从坐标）',),loc='upper right')
        plt.title(r'Jimu与Radar纵向（Y)）测速对比')
        plt.savefig(os.path.join(DataFolder, fileID + '_Speed_Y_01_OverView.png'))
        print('Jimu与Radar纵向（Y)）测速对比对比图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Speed_Y_01_OverView.png'))

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        Data_longtitudinalDistanceToFrameIndex.plot(x='frame index', y=['h_speed', 'obj_x_vrel'], style=['b', 'r'],kind='line',ax=ax1)
        Data_longtitudinalDistanceToFrameIndex.plot(x='frame index', y=['Radar'], style=['k--'],
                                                    kind='line', ax=ax2)
        ax1.legend_.remove()
        ax1.set_xlabel(r'frame index')
        ax1.set_ylabel(r'横向相对速度（X）')
        ax1.legend(labels=('Jimu相对速度值', 'Radar相对速度值'), loc='upper left')
        ax1.grid()
        ax2.legend_.remove()
        ax2.set_xlabel(r'frame index')
        ax2.set_ylabel(r'从坐标：纵向距离')
        ax2.legend(labels=(r'纵向距离（从坐标）',), loc='upper right')
        plt.title(r'Jimu与Radar横向（X)测速对比')
        plt.savefig(os.path.join(DataFolder, fileID + '_Speed_X_01_OverView.png'))
        print('Jimu与Radar横向（X)测速对比图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Speed_X_01_OverView.png'))

    Data_intersection = Data_union.dropna()
    Data_intersection = Data_intersection[
        (Data_intersection['frame_index'] >= framestart) & (Data_intersection['frame_index'] <= frameend)]
    Data_details = Data_intersection.rename(columns={
        'objId':'Jimu ID',
    'v_dist':'Jimu y distance',
    'h_dist':'Jimu x distance',
    'v_speed':'Jimu y speed',
    'h_speed':'Jimu x speed',
    'width':'Jimu Object width',
    'height':'Jimu Object height',
    'obj_id':'Radar ID',
    'obj_x':'Radar x distance',
    'obj_y':'Radar y distance',
    'obj_x_vrel':'Radar x speed',
    'obj_y_vrel':'Radar y speed',
    })
    Data_details.to_csv(os.path.join(DataFolder,fileID+'_details.csv'),index=False,encoding='utf_8_sig')
    print('Jimu和Radar的距离对比详细数据信息保存至' + os.path.join(DataFolder, fileID + '_details.csv'))

    if mode==0:
        Data_ErrorPDFCDF = Data_intersection[['frame_index', 'v_dist', 'obj_y', 'h_dist', 'obj_x']].rename(
            columns={'frame_index': 'frame index', 'v_dist': 'Jimu', 'obj_y': 'Radar'})
        Data_ErrorPDFCDF['error'] = (Data_ErrorPDFCDF['Jimu'] - Data_ErrorPDFCDF['Radar']) / Data_ErrorPDFCDF[
            'Radar'] * 100
        Data_ErrorPDFCDF['error_X'] = (Data_ErrorPDFCDF['h_dist'] - Data_ErrorPDFCDF['obj_x']) / Data_ErrorPDFCDF[
            'obj_x'] * 100
        Data_ErrorPDFCDF.sort_values(by=['Radar'], inplace=True)
        Data_ErrorPDFCDF['Threshold_high'] = 5
        Data_ErrorPDFCDF['Threshold_low'] = -5
        Data_ErrorPDFCDF.plot(x='Radar', y=['error', 'Threshold_high', 'Threshold_low'], style=['b', 'r--', 'r--'])
        ax = plt.axes()
        ax.legend_.remove()
        plt.grid()
        plt.xlabel(r'distance / m')
        plt.ylabel(r'error / %')
        plt.title(r'Jimu纵向（Y）测距误差随距离的变化')
        plt.savefig(os.path.join(DataFolder, fileID + '_Distance_Y_02_error.png'))
        print('Jimu纵向（Y）测距误差随距离的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_02_error.png'))

        Data_ErrorPDFCDF.sort_values(by=['obj_x'], inplace=True)
        Data_ErrorPDFCDF.plot(x='obj_x', y=['error_X', 'Threshold_high', 'Threshold_low'], style=['b', 'r--', 'r--'])
        ax = plt.axes()
        ax.legend_.remove()
        plt.grid()
        plt.xlabel(r'distance / m')
        plt.ylabel(r'error / %')
        plt.title(r'Jimu横向（X）测距误差随距离的变化')
        plt.savefig(os.path.join(DataFolder, fileID + '_Distance_X_02_error.png'))
        print('Jimu横向（X）测距误差随距离的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_X_02_error.png'))

        fig, axes = plt.subplots(1, 2)
        Data_ErrorPDFCDF.plot(y='error', kind='hist', facecolor='red', bins=100, ax=axes[0])
        # ax = plt.axes()
        axes[0].legend_.remove()
        axes[0].set_xlabel(r'error / %')
        axes[0].set_ylabel(r'')
        axes[0].set_title(r'PDF')

        Data_ErrorPDFCDF['error'] = abs(Data_ErrorPDFCDF['error'])
        Data_ErrorPDFCDF.plot(y='error', kind='hist', cumulative=True, density=1, bins=1000, ax=axes[1],
                              histtype='step',
                              color='coral')
        axes[1].set_xlim(0, Data_ErrorPDFCDF['error'].max())
        axes[1].set_ylim(0, 1)
        axes[1].legend_.remove()
        axes[1].set_xlabel(r'error / %')
        axes[1].set_ylabel(r'')
        axes[1].grid()
        axes[1].set_title(r'Empirical CDF')
        fig.suptitle('误差分布')
        plt.savefig(os.path.join(DataFolder, fileID + '_Distance_Y_03_CDF&PDF.png'))
        print('误差分布图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_03_CDF&PDF.png'))

    if mode==1:
        Data_ErrorPDFCDF = Data_intersection[['frame_index', 'v_dist', 'obj_y', 'h_dist', 'obj_x']].rename(
            columns={'frame_index': 'frame index', 'v_dist': 'Jimu', 'obj_y': 'Radar'})
        Data_ErrorPDFCDF['error'] = (Data_ErrorPDFCDF['Jimu'] - Data_ErrorPDFCDF['Radar']) / Data_ErrorPDFCDF[
            'Radar'] * 100
        Data_ErrorPDFCDF['error_X'] = (Data_ErrorPDFCDF['h_dist'] - Data_ErrorPDFCDF['obj_x']) / Data_ErrorPDFCDF[
            'obj_x'] * 100
        #Data_ErrorPDFCDF.sort_values(by=['Radar'], inplace=True)
        Data_ErrorPDFCDF['Threshold_high'] = 5
        Data_ErrorPDFCDF['Threshold_low'] = -5
        Data_ErrorPDFCDF.plot(x='frame index', y=['error', 'Threshold_high', 'Threshold_low'], style=['b', 'r--', 'r--'])
        ax = plt.axes()
        ax.legend_.remove()
        plt.grid()
        plt.xlabel(r'frame index / m')
        plt.ylabel(r'error / %')
        plt.title(r'Jimu纵向（Y）测距误差随时间（frame index）的变化')
        plt.savefig(os.path.join(DataFolder, fileID + '_Distance_Y_02_error.png'))
        print('Jimu纵向（Y）测距误差随时间（frame index）的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_02_error.png'))

        Data_ErrorPDFCDF.plot(x='frame index', y=['error_X', 'Threshold_high', 'Threshold_low'], style=['b', 'r--', 'r--'])
        ax = plt.axes()
        ax.legend_.remove()
        plt.grid()
        plt.xlabel(r'frame index / m')
        plt.ylabel(r'error / %')
        plt.title(r'Jimu横向（X）测距误差随时间（frame index）的变化')
        plt.savefig(os.path.join(DataFolder, fileID + '_Distance_X_02_error.png'))
        print('Jimu横向（X）测距误差随时间（frame index）的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_X_02_error.png'))

        fig, axes = plt.subplots(1, 2)
        Data_ErrorPDFCDF.plot(y='error', kind='hist', facecolor='red', bins=100, ax=axes[0])
        # ax = plt.axes()
        axes[0].legend_.remove()
        axes[0].set_xlabel(r'error / %')
        axes[0].set_ylabel(r'')
        axes[0].set_title(r'PDF')

        Data_ErrorPDFCDF['error'] = abs(Data_ErrorPDFCDF['error'])
        Data_ErrorPDFCDF.plot(y='error', kind='hist', cumulative=True, density=1, bins=1000, ax=axes[1],
                              histtype='step',
                              color='coral')
        axes[1].set_xlim(0, Data_ErrorPDFCDF['error'].max())
        axes[1].set_ylim(0, 1)
        axes[1].legend_.remove()
        axes[1].set_xlabel(r'error / %')
        axes[1].set_ylabel(r'')
        axes[1].grid()
        axes[1].set_title(r'Empirical CDF')
        fig.suptitle('纵向（Y）误差分布')
        plt.savefig(os.path.join(DataFolder, fileID + '_Distance_Y_03_CDF&PDF.png'))
        print('纵向（Y）误差分布图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_03_CDF&PDF.png'))

        # fig, axes = plt.subplots(1, 2)
        # Data_ErrorPDFCDF.plot(y='error_X', kind='hist', facecolor='red', bins=100, ax=axes[0])
        # # ax = plt.axes()
        # axes[0].legend_.remove()
        # axes[0].set_xlabel(r'error / %')
        # axes[0].set_ylabel(r'')
        # axes[0].set_title(r'PDF')
        #
        # Data_ErrorPDFCDF['error_X'] = abs(Data_ErrorPDFCDF['error_X'])
        # Data_ErrorPDFCDF.plot(y='error_X', kind='hist', cumulative=True, density=1, bins=1000, ax=axes[1],
        #                       histtype='step',
        #                       color='coral')
        # axes[1].set_xlim(0, Data_ErrorPDFCDF['error_X'].max())
        # axes[1].set_ylim(0, 1)
        # axes[1].legend_.remove()
        # axes[1].set_xlabel(r'error / %')
        # axes[1].set_ylabel(r'')
        # axes[1].grid()
        # axes[1].set_title(r'Empirical CDF')
        # fig.suptitle('横向（X）误差分布')
        # plt.savefig(os.path.join(DataFolder, fileID + '_Distance_X_03_CDF&PDF.png'))
        # print('横向（X）误差分布图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_X_03_CDF&PDF.png'))


    if drawSpeed:
        if mode==0:
            Data_ErrorPDFCDF = Data_intersection[['obj_y', 'v_speed', 'obj_y_vrel']].rename(
                columns={'obj_y': 'distance', 'v_speed': 'Jimu', 'obj_y_vrel': 'Radar'})
            Data_ErrorPDFCDF['error'] = (Data_ErrorPDFCDF['Jimu'] - Data_ErrorPDFCDF['Radar']) / Data_ErrorPDFCDF[
                'Radar'] * 100
            # Data_ErrorPDFCDF.sort_values(by=['Radar'], inplace=True)
            Data_ErrorPDFCDF['Threshold_high'] = 5
            Data_ErrorPDFCDF['Threshold_low'] = -5
            Data_ErrorPDFCDF.plot(x='distance', y=['error', 'Threshold_high', 'Threshold_low'],
                                  style=['b', 'r--', 'r--'])
            ax = plt.axes()
            ax.legend_.remove()
            plt.grid()
            plt.xlabel(r'distance / m')
            plt.ylabel(r'longitudinal speed error / %')
            plt.title(r'Jimu纵向相对速度（Y）误差随距离的变化')
            plt.savefig(os.path.join(DataFolder, fileID + '_Speed_Y_02_error.png'))
            print('Jimu纵向相对速度（Y）误差随距离的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Speed_Y_02_error.png'))
            Data_ErrorPDFCDF = Data_intersection[['obj_y', 'h_speed', 'obj_x_vrel']].rename(
                columns={'obj_y': 'distance', 'h_speed': 'Jimu', 'obj_x_vrel': 'Radar'})
            Data_ErrorPDFCDF['error'] = (Data_ErrorPDFCDF['Jimu'] - Data_ErrorPDFCDF['Radar']) / Data_ErrorPDFCDF[
                'Radar'] * 100
            # Data_ErrorPDFCDF.sort_values(by=['Radar'], inplace=True)
            Data_ErrorPDFCDF['Threshold_high'] = 5
            Data_ErrorPDFCDF['Threshold_low'] = -5
            Data_ErrorPDFCDF.plot(x='distance', y=['error', 'Threshold_high', 'Threshold_low'],
                                  style=['b', 'r--', 'r--'])
            ax = plt.axes()
            ax.legend_.remove()
            plt.grid()
            plt.xlabel(r'distance / m')
            plt.ylabel(r'Horizontal speed error / %')
            plt.title(r'Jimu横向相对速度（x）误差随距离的变化')
            plt.savefig(os.path.join(DataFolder, fileID + '_Speed_X_02_error.png'))
            print('Jimu横向相对速度(x)误差随距离的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Speed_X_02_error.png'))

        if mode==1:
            Data_ErrorPDFCDF = Data_intersection[['frame_index', 'v_speed', 'obj_y_vrel']].rename(
                columns={'frame_index': 'frame index', 'v_speed': 'Jimu', 'obj_y_vrel': 'Radar'})
            Data_ErrorPDFCDF['error'] = (Data_ErrorPDFCDF['Jimu'] - Data_ErrorPDFCDF['Radar']) / Data_ErrorPDFCDF[
                'Radar'] * 100
            # Data_ErrorPDFCDF.sort_values(by=['Radar'], inplace=True)
            Data_ErrorPDFCDF['Threshold_high'] = 5
            Data_ErrorPDFCDF['Threshold_low'] = -5
            Data_ErrorPDFCDF.plot(x='frame index', y=['error', 'Threshold_high', 'Threshold_low'],
                                  style=['b', 'r--', 'r--'])
            ax = plt.axes()
            ax.legend_.remove()
            plt.grid()
            plt.xlabel(r'frame index / m')
            plt.ylabel(r'longitudinal speed error / %')
            plt.title(r'Jimu纵向相对速度（Y）误差随时间（frame index）的变化')
            plt.savefig(os.path.join(DataFolder, fileID + '_Speed_Y_02_error.png'))
            print('Jimu纵向相对速度（Y）误差随时间（frame index）的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Speed_Y_02_error.png'))
            Data_ErrorPDFCDF = Data_intersection[['frame_index', 'h_speed', 'obj_x_vrel']].rename(
                columns={'frame_index': 'frame index', 'h_speed': 'Jimu', 'obj_x_vrel': 'Radar'})
            Data_ErrorPDFCDF['error'] = (Data_ErrorPDFCDF['Jimu'] - Data_ErrorPDFCDF['Radar']) / Data_ErrorPDFCDF[
                'Radar'] * 100
            # Data_ErrorPDFCDF.sort_values(by=['Radar'], inplace=True)
            Data_ErrorPDFCDF['Threshold_high'] = 5
            Data_ErrorPDFCDF['Threshold_low'] = -5
            Data_ErrorPDFCDF.plot(x='frame index', y=['error', 'Threshold_high', 'Threshold_low'],
                                  style=['b', 'r--', 'r--'])
            ax = plt.axes()
            ax.legend_.remove()
            plt.grid()
            plt.xlabel(r'frame index / m')
            plt.ylabel(r'Horizontal speed error / %')
            plt.title(r'Jimu横向相对速度（x）误差随时间（frame index）的变化')
            plt.savefig(os.path.join(DataFolder, fileID + '_Speed_X_02_error.png'))
            print('Jimu横向相对速度(x)误差随时间（frame index）的变化图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Speed_X_02_error.png'))




    df_staticStage = df_IDSelect[['static start frame', 'static end frame']].dropna()
    if len(df_staticStage) == 0:
        print(os.path.join(DataFolder, filename) + '统计完毕！')
        return
    cutlist = []
    for k in range(len(df_staticStage)):
        cutlist.append((df_staticStage.iloc[k,0],df_staticStage.iloc[k,1]))
    bins = pd.IntervalIndex.from_tuples(cutlist,closed='both')
    StaticStageCategories = pd.cut(Data_ErrorPDFCDF['frame index'],bins)
    Data_static = Data_ErrorPDFCDF.groupby(StaticStageCategories).agg({
        'Jimu':[np.mean,np.std],
        'Radar':[np.mean,np.std]
    })

    Data_staticindex = Data_static.index
    Name=[]
    for k in range(len(Data_staticindex)):
        for k1 in range(len(StageName)):
            if StageName.iloc[k1]['frameindex'] in Data_staticindex[k]:
                Name.append(StageName.iloc[k1]['Name'])
                break
    Data_static['Name'] = Name
    Data_static['average error'] = (Data_static[('Jimu','mean')]-Data_static[('Radar','mean')])/Data_static[('Radar','mean')]*100
    Data_static.plot(x='Name',y=[('Jimu', 'mean'),('Radar','mean')],style=['bo-', 'rX-'], kind='line')
    plt.legend(('Jimu','Radar'))
    plt.grid()
    plt.xlabel(r'')
    plt.ylabel(r'average distance / m')
    plt.title(r'静态测距:Jimu与Radar均值对比')
    plt.savefig(os.path.join(DataFolder,fileID+'_Distance_Y_04_StaticAverageDistance.png'))
    print('静态测距:Jimu与Radar均值对比图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_04_StaticAverageDistance.png'))

    Data_static.plot(x=('Radar','mean'),y=[('Jimu','std'),('Radar','std')],style=['bo-','rX-'])
    plt.legend(('Jimu','Radar'))
    plt.grid()
    plt.xlabel(r'distance / m')
    plt.ylabel(r'standard')
    plt.title(r'静态测距：Jimu与Radar标准差对比')
    plt.savefig(os.path.join(DataFolder,fileID+'_Distance_Y_05_StaticStandard.png'))
    print('静态测距：Jimu与Radar标准差对比图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_05_StaticStandard.png'))

    Data_static.plot(x=('Radar','mean'),y=['average error'],style='bo-')
    ax = plt.axes()
    ax.legend_.remove()
    plt.grid()
    plt.xlabel(r'distance / m')
    plt.ylabel(r'average error / %')
    plt.title(r'静态测距：Jimu测距平均误差')
    plt.savefig(os.path.join(DataFolder,fileID+'_Distance_Y_06_StaticAverageError.png'))
    print('静态测距：Jimu测距平均误差图  生成成功，保存至' + os.path.join(DataFolder, fileID + '_Distance_Y_06_StaticAverageError.png'))
    print( os.path.join(DataFolder, filename) +'统计完毕！')






