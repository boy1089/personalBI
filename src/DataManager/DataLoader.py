

import pandas as pd
import os
import glob

import src.util as util



class DataLoader:
    def loadData(self):
        folders =  glob.glob(util.path_log)
        folder = [x for x in folders if x.find('processedData') != -1][0]
        files = glob.glob(folder + r'/*.csv')

        file_summary = [x for x in files if x.find('raw2') != -1 ][0]
        df = pd.read_csv(file_summary)

        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        # df = df.sort_index()
        return df


if __name__ == "__main__":
    dataLoader = DataLoader()
    df = dataLoader.loadData()

    #previous plots
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import cm

    #daiy plot
    # fig, ax = plt.subplots(subplot_kw = {'projection': 'polar'})
    # df_temp = df['20220825']
    # df_temp = df_temp.sort_index()
    # df_temp['theta'] = np.arange(0, len(df_temp))/len(df_temp) * 2* np.pi - 1/2*np.pi
    # df_temp['num'] = np.arange(0, len(df_temp))
    # # df_temp = df_temp.apply(pd.to_numeric, errors = 'coerce')
    # parameter = 'latitude'
    # df_temp['test'] = (df_temp[parameter] - df_temp[parameter].min() + 0.1)
    # # ax.scatter(df_temp['theta'], df_temp['test']/df_temp['test'].max(), c = cm.hot(np.abs(df_temp['accelX'].diff().values)/2), s = 1)
    # ax.scatter(df_temp['theta'], [1]*df_temp['theta'].shape[0],c=cm.hot(np.abs(df_temp['latitude'].values - df_temp['latitude'].mean()) / 0.2), s=1)
    #
    # df_files = df_temp[['file', 'theta', 'num']].dropna()
    # for i in range(len(df_files)):
    #     ax.plot([df_files['theta'][i]]*2, [1, 1.05], c = 'blue')
    # ax.set_rlim(0, 1.5)
    # ax.set_xticklabels([ '6', '', '12', '', '18', '','0', '',])
    # ax.set_rticks([])
    # ax.grid(True)
    # ax.set_theta_direction(-1)

    #montly plot
    fig, ax = plt.subplots(subplot_kw = {'projection': 'polar'})
    # df_temp = df['20220821':"20220827"]
    # df_temp = df['20220807':"20220813"]
    df_temp = df['20220801':"20220830"]
    df_temp = df_temp.sort_index()
    df_temp['theta'] = np.arange(0, len(df_temp))/len(df_temp) * 2* np.pi - 1/2*np.pi
    df_temp['num'] = np.arange(0, len(df_temp))
    # df_temp = df_temp.apply(pd.to_numeric, errors = 'coerce')
    parameter = 'latitude'
    df_temp['test'] = (df_temp[parameter] - df_temp[parameter].min() + 0.1)
    # ax.scatter(df_temp['theta'], df_temp['test']/df_temp['test'].max(), c = cm.hot(np.abs(df_temp['accelX'].diff().values)/2), s = 1)
    df_theta = df_temp[['theta', 'latitude', 'longitude']][::50]

    print(df_theta.shape[0])
    ax.scatter(df_theta['theta'], [1]*df_theta.shape[0],c=cm.hot(np.abs(df_theta['latitude'].values - df_theta['latitude'].mean()) / 0.2), s=50)
    print(df_temp.columns)

    df_files = df_temp[['file', 'theta', 'num']].dropna()
    for i in range(len(df_files)):
        ax.plot([df_files['theta'][i]]*2, [1.1, 1.2], c = 'blue')
    print(df_temp['phoneNumber'].dropna())

    df_call = df_temp[['theta', 'num', 'phoneNumber']].dropna()
    for i in range(len(df_call)):
        ax.plot([df_call['theta'][i]] * 2, [1.3, 1.4], c='red')
    print(df_temp.columns)

    df_expense = df_temp[['theta', 'num', '출금액']].dropna()
    for i in range(len(df_expense)):
        ax.plot([df_expense['theta'][i]] * 2, [1.5, 1.6], c='black')


    ax.set_rlim(0, 2.0)
    ax.set_xticklabels([])
    ax.set_rticks([], [])
    ax.grid(False)
    ax.set_theta_direction(-1)



    print('a')

    print('b')