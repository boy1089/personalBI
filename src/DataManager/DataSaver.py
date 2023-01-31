

import pandas as pd
import os
import src.util as util
import glob



class DataSaver:


    def saveData(self, df, filename):
        path = util.path_log
        folders = glob.glob(path)
        folder_save = [x for x in folders if x.find('processedData') != -1][0]
        df['time'] = df.index
        df.to_csv(fr'{folder_save}/{filename}')
        return df


if __name__ == "__main__":
    print('aa')