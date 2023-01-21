from src.DataManager import DataReader
import matplotlib.pyplot as plt




columnsDefault = [
    'longitude',
    'latitude',
    'accelX',
    'accelY',
    'accelZ'
]
class DataViewer:

    def __init__(self, data):
        self.data = data

    def plotDate(self, date):
        plt.plot()


if __name__ == '__main__':

    dataReader = DataReader.DataReader()
    data = dataReader.mergeData()
    print(data)
    data2 = data['2020':'2022']
    plt.plot(data2[data2['은행'] == 'kb']['잔액'])
    plt.plot(data2['latitude'].dropna().sort_index())
