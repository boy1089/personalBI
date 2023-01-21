

#TODO : implement calmap with selectable index
#TODO : create event --> link to dayily view
#TODO : Design daily view. (timeline, image, location, event) -- ㅡ make note regularly,

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import numpy as np
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
from src.DataManager import DataAnalyzer, DataLoader
import calmap

from matplotlib import rc

rc('font',family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

class MyApp(QMainWindow):


    def __init__(self):

        super().__init__()
        # dataReader = DataReader.DataReader()
        dataLoader = DataLoader.DataLoader()
        self.data = dataLoader.loadData()


        # self.data = dataReader.mergeData()
        self.dataAnalyzer = DataAnalyzer.DataAnalyzer(self.data)

        self.dataList = self.data.columns
        self.setUi()

    def setUi(self):
        self.setGeometry(0, 0, 2000, 1000)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.canvas = FigureCanvas(Figure(figsize=(12, 12)))
        self.canvas2 = FigureCanvas(Figure(figsize = (4, 8)))

        self.hbox = QHBoxLayout(self.main_widget)

        self.gridbox = QGridLayout()
        self.comboBox = QComboBox()

        for i, item in enumerate(['day', 'week']):
            self.comboBox.addItem(item)

        self.comboBox.currentIndexChanged.connect(self.comboBoxFunction)

        self.btn = QPushButton('single plot')
        # self.btn = QPushButton('merged plot')

        self.btn.clicked.connect(self.btnClicked)

        self.datetimeEdit = QDateTimeEdit()
        # self.datetimeEdit.setDisplayFormat('yyyy.MM.dd')
        self.datetimeEdit.setDisplayFormat('MM.dd')

        self.datetimeEdit.setDateTime(QDateTime(QDate(2022, 7, 1)))
        self.datetimeEdit.dateChanged.connect(self.selectDate)

        self.gridbox.addWidget(self.canvas2)
        self.gridbox.addWidget(self.btn)
        self.gridbox.addWidget(self.comboBox)
        self.gridbox.addWidget(self.datetimeEdit)

        self.hbox.addWidget(self.canvas)
        self.hbox.addLayout(self.gridbox)

        self.setLayout(self.hbox)

        self.addToolBar(NavigationToolbar(self.canvas, self))

        self.ax = self.canvas.figure.subplots(4, 1, sharex = True, gridspec_kw = {'height_ratios' : [1, 1, 1, 10]})
        self.ax3 = self.ax[2].twinx()

        self.ax4 = self.canvas2.figure.subplots(1, 1)

        self.selectDate()
        self.plotYearPlot()
        self.setWindowTitle('Matplotlib in PyQt5')


        self.show()
        self.canvas.mpl_connect('button_press_event', self.click)

        self.canvas2.mpl_connect('button_press_event', self.click_yearplot)

    def plotYearPlot(self):

        summaryOfDates = self.dataAnalyzer.getSummaryOfDates("20220101", "20220830")
        # summaryOfDates = self.dataAnalyzer.getSummaryOfDates("20210101", "20211231")


        summaryOfDates.index = [x.to_pydatetime() for x in summaryOfDates.index]
        # calmap.yearplot(summaryOfDates[summaryOfDates.columns[9]],  dayticks= False, monthticks= False, ax = self.ax4)
        print("summaryOfDates");
        print(summaryOfDates)
        ax, plot_data, colormesh = calmap.yearplot(summaryOfDates[summaryOfDates.columns[5]], dayticks=False, monthticks=False, ax=self.ax4)
        self.canvas2.figure.colorbar(colormesh)

    def click_yearplot(self, event):
        print(event.xdata, event.ydata)

        print(-1* int(event.xdata) + 7*int(event.ydata) +1)
        week = int(event.ydata)
        day = int(event.xdata) * -1

        clickedDay = 7*week + day +1
        clickedDate = datetime.datetime(2022, 1, 1) + datetime.timedelta(days = clickedDay)
        QDate_clickedDate = QDateTime(QDate(2022, clickedDate.month, clickedDate.day))
        self.datetimeEdit.setDateTime(QDate_clickedDate)


    def btnClicked(self):
        print(self.btn.text())
        if self.btn.text() == 'single plot':
            self.btn.setText('merged plot')
            self.comboBox.setDisabled(True)
            self.comboBox.setCurrentText('week')

        else :
            self.btn.setText('single plot')
            self.comboBox.setDisabled(False)

    def drawAxes(self):
        self.drawAx0()
        self.drawAx1()
        self.drawAx2()
        self.drawAx3()

        self.ax[0].grid()
        self.ax[1].grid()
        self.ax[2].grid()
        self.ax[3].grid()

        self.canvas.draw()

    def selectDate(self):
        print(self.datetimeEdit.date().toString('yyyyMMdd'))

        if self.comboBox.currentText() == 'day':
            self.date = self.datetimeEdit.date().toString('yyyyMMdd')
            self.selectedData = [self.data.loc[self.date].sort_index()]

        if self.comboBox.currentText() == 'week':
            self.date = self.datetimeEdit.date().toString('yyyyMMdd')
            result = datetime.date(int(self.date[:4]), int(self.date[4:6]), int(self.date[6:8])).isocalendar()
            year = result[0]
            week = result[1]
            startDate = datetime.date.fromisocalendar(year, week, 1).strftime('%Y%m%d')
            endDate = datetime.date.fromisocalendar(year, week, 7).strftime('%Y%m%d')
            self.selectedData = [self.data[startDate:endDate]]

        if self.btn.text() == 'merged plot':
            data_temp = {}
            for day in range(1, 8):
                date = datetime.date.fromisocalendar(year, week, day).strftime('%Y%m%d')

                data_temp[date] = self.selectedData[0].loc[date]
                data_temp[date].index = [datetime.datetime.combine(datetime.date(1970, 1, 1), x.time()) for x in data_temp[date].index]
            self.selectedData = data_temp

        self.drawAxes()

    def drawAx0(self):
        colors1 = ['C{}'.format(i) for i in range(6)]
        if self.btn.text() == 'single plot':
            self.ax[0].cla()
            self.ax[0].eventplot(self.selectedData[0]['입금액'].replace(0, np.nan).dropna().index.values, colors=[colors1[0]], lineoffsets=[0.25],
                                 linelengths=[0.5], orientation='horizontal')
            self.ax[0].eventplot(self.selectedData[0]['출금액'].replace(0, np.nan).dropna().index.values, colors=[colors1[1]], lineoffsets=[-0.25],
                                 linelengths=[0.5], orientation='horizontal')

            self.ax[0].eventplot(self.selectedData[0]['name'].replace(0, np.nan).dropna().index.values,
                                 colors=[colors1[1]], lineoffsets=[0.5],
                                 linelengths=[0.5], orientation='horizontal')

            for i, name in enumerate(self.selectedData[0]['name'].dropna().values):
                self.ax[0].text(self.selectedData[0]['name'].dropna().index.values[i], 0.5, name)

            for i, input in enumerate(self.selectedData[0]['note'].dropna().values):
                self.ax[0].text(self.selectedData[0]['note'].dropna().index.values[i], 0, input)

            self.ax[0].set_ylim(-1, 1)

            try :
                self.ax[0].set_xlim(self.selectedData[0].index[0].date(), (self.selectedData[0].index[-1]+ datetime.timedelta(days=1)).date())
            except :
                pass

        if self.btn.text() == 'merged plot':
            self.ax[0].cla()
            for i, date in enumerate(self.selectedData.keys()):
                self.ax[0].eventplot(self.selectedData[date]['입금액'].replace(0, np.nan).dropna().index.values,
                                     colors=[colors1[0]], lineoffsets=[0.25+0.05*i],
                                     linelengths=[0.5], orientation='horizontal')

                self.ax[0].eventplot(self.selectedData[date]['출금액'].replace(0, np.nan).dropna().index.values,
                                     colors=[colors1[1]], lineoffsets=[-0.25+0.05*i],
                                     linelengths= [0.5], orientation='horizontal')

            self.ax[0].set_ylim(-1, 1)

            self.ax[0].set_xlim(datetime.date(1970, 1, 1), datetime.date(1970, 1, 2))
            myFmt = DateFormatter("%H")
            self.ax[0].xaxis.set_major_formatter(myFmt)




    def drawAx1(self):

        if self.btn.text() == 'single plot':
            self.ax[1].cla()
            self.ax[1].plot(self.selectedData[0]['accelX'].dropna(), label = 'x')
            self.ax[1].plot(self.selectedData[0]['accelY'].dropna(), label = 'y')
            self.ax[1].plot(self.selectedData[0]['accelZ'].dropna(), label = 'z')

            self.ax[1].set_ylim(-20, 20)
            self.ax[1].legend()

        if self.btn.text() == 'merged plot':
            self.ax[1].cla()

            for i, date in enumerate(self.selectedData.keys()):
                # self.ax[1].plot(self.selectedData[date]['accelX'].dropna(), label='x')
                # self.ax[1].plot(self.selectedData[date]['accelY'].dropna(), label='y')
                self.ax[1].plot(self.selectedData[date]['accelZ'].dropna(), label='z')

            self.ax[1].set_ylim(-20, 20)
            # self.ax[1].legend()

    def drawAx2(self):
        if self.btn.text() == 'single plot':
            self.ax[2].cla()
            self.ax[2].plot(self.selectedData[0]['latitude'].dropna())
            self.ax3.cla()
            self.ax3.plot(self.selectedData[0]['longitude'].dropna())

        if self.btn.text() == 'merged plot':
            self.ax[2].cla()
            self.ax3.cla()
            for i, date in enumerate(self.selectedData.keys()):
                self.ax[2].plot(self.selectedData[date]['latitude'].dropna(), label = date)

                # self.ax3.cla()
                # self.ax3.plot(self.selectedData[date]['longitude'].dropna())
            self.ax[2].legend()

    def drawAx3(self):

        print('drawing image axis, ax[0]..')

        data = self.selectedData[0]['file'].replace(0, np.nan).dropna()
        if self.btn.text() == 'single plot':
            self.ax[3].cla()
            self.ax[3].eventplot(data.index.values,
                                 lineoffsets=[0.25],
                                 linelengths=[0.5], orientation='horizontal')

        if self.btn.text() == 'merged plot':
            self.ax[3].cla()
            for i, date in enumerate(self.selectedData.keys()):
                self.ax[3].eventplot(data.index.values,
                                     lineoffsets=[0.25],
                                     linelengths=[0.5], orientation='horizontal')

        self.boxAll = []
        positionList = [0.25, 0.5 , 0.75, 0]

        rand = 0
        for i, (date, file) in enumerate(zip(data.index.values, data.values)):
            img = plt.imread(file)[::7, ::7, :]
            self.im = OffsetImage(img)
            print(date, file)
            try :
                sec =     (data.index.values[i+1] - data.index.values[i]).astype('timedelta64[s]') / np.timedelta64(1, 's')
                timeDiff = datetime.timedelta(seconds = sec)
            except :
                timeDiff = datetime.timedelta(hours= 0.1)
            print(timeDiff)

            if timeDiff > datetime.timedelta(hours = 1):
                rand = 0
            else :
                rand +=1


            # locationOfBox = (mdates.date2num(date) + (np.random.rand()-0.5)/5  + (rand//4)/5, positionList[np.mod(i, 4)])
            locationOfBox = (mdates.date2num(date)  + ((rand//4)-1) * 1/20, positionList[np.mod(i, 4)])

            box1 = AnnotationBbox(self.im, (mdates.date2num(date), 0.5), xybox= locationOfBox, xycoords='data', boxcoords='data', pad=0.3)

            self.ax[3].add_artist(box1)
            # self.ax[3].add_artist(box2)
            self.boxAll.append(box1)

            box1.set_visible(True)
            # box2.set_visible(True)
        self.ax[3].grid(False)


    def comboBoxFunction(self):
        self.ax[1].cla()
        self.ax[2].cla()

        # self.ax.plot(self.data[self.comboBox.currentText()].dropna().sort_index(), '-')
        print(self.comboBox.currentText())
        self.canvas.draw()


    def getMergedData(self):
        pass

    def click(self, event):
        print(event.xdata, event.ydata)
        print(mdates.num2date(event.xdata))


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())



