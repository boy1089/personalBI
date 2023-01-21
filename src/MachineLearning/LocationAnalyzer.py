
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import DBSCAN
import src.util as util
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.pyplot as plt


#TODO : seperate moving state from -1
def classifyLocations(df, locationClassifications, threshold = 1000, numberOfCluster = 10):
    '''

    :param df: dataframe
    :return: data from with additional column 'classifciation'
     -1 : not classified, mostly moving
      other integers : classified.
    '''
    # df = df[['latitude', 'longitude']].dropna()
    kmeans = KMeans(n_clusters=numberOfCluster, init='k-means++', max_iter=300, random_state=0)
    kmeans.fit(df[['longitude', 'latitude']])

    df['classification'] = -1
    setOfClassification = list(set(kmeans.labels_))
    for i, classification in enumerate(setOfClassification):
        index = util.find_indices(kmeans.labels_, classification)
        if(len(index) < threshold): continue
        # plt.scatter(df['latitude'][index], df['longitude'][index], s = 1)
        latitudeMedian = round(df['latitude'][index].median(), 2)
        longitudeMedian = round(df['longitude'][index].median(), 2)


        classifier = findLocationClassifier(locationClassifications, [latitudeMedian, longitudeMedian])
        df['classification'][index] = classifier

        locationClassifications[classifier] = [latitudeMedian, longitudeMedian]

    return df, locationClassifications


def classifyLocations_MeanShift(df, locationClassifications, threshold = 1, bandwidth = None):
    '''

    :param df: dataframe
    :return: data from with additional column 'classifciation'
     -1 : not classified, mostly moving
      other integers : classified.
    '''
    df = df[['latitude', 'longitude']].dropna()
    data = np.asarray([list(df['latitude'].values), list(df['longitude'].values)]).T
    print("estimating bandwidth..")
    if bandwidth ==None :
        bandwidth = estimate_bandwidth(data)
    # print(f"estimating bandwidth done, bandwidth : {bandwidth}")
    print("process MeanShift..")
    meanshift = MeanShift(bandwidth = bandwidth)
    labels = meanshift.fit_predict(data)
    print("done")
    df['classification'] = -1
    setOfClassification = list(set(labels))
    for i, classification in enumerate(setOfClassification):
        index = util.find_indices(labels, classification)
        if(len(index) < threshold): continue
        # plt.scatter(df['latitude'][index], df['longitude'][index], s = 1)
        latitudeMedian = round(df['latitude'][index].median(), 2)
        longitudeMedian = round(df['longitude'][index].median(), 2)


        classifier = findLocationClassifier(locationClassifications, [latitudeMedian, longitudeMedian])
        df['classification'][index] = classifier

        locationClassifications[classifier] = [latitudeMedian, longitudeMedian]

    return df, locationClassifications


def classifyLocations_DBSCAN(df, locationClassifications, threshold = 1, bandwidth = None):
    '''

    :param df: dataframe
    :return: data from with additional column 'classifciation'
     -1 : not classified, mostly moving
      other integers : classified.
    '''
    df = df[['latitude', 'longitude']].dropna()
    data = np.asarray([list(df['latitude'].values), list(df['longitude'].values)]).T
    dbscan = DBSCAN(eps = 1, min_samples = 1, metric = 'euclidean')

    labels = dbscan.fit_predict(data)
    print("done")
    df['classification'] = -1
    setOfClassification = list(set(labels))
    for i, classification in enumerate(setOfClassification):
        index = util.find_indices(labels, classification)
        if(len(index) < threshold): continue
        # plt.scatter(df['latitude'][index], df['longitude'][index], s = 1)
        latitudeMedian = round(df['latitude'][index].median(), 2)
        longitudeMedian = round(df['longitude'][index].median(), 2)


        classifier = findLocationClassifier(locationClassifications, [latitudeMedian, longitudeMedian])
        df['classification'][index] = classifier

        locationClassifications[classifier] = [latitudeMedian, longitudeMedian]

    return df, locationClassifications


def findLocationClassifier(locationClassifications, latLongList):
    classifier = -1
    for i, classifier in enumerate(locationClassifications):
        isMatch = locationClassifications[classifier] == latLongList

        if isMatch :
            return classifier
    print('aa')
    print(classifier)
    return classifier + 1

def eventPlotLocation(ax, df, classificationResult, offset = 0):
    # colors = ['blue', 'red', 'orange', 'green', 'purple', 'grey', 'black']
    colors = list(mcolors.TABLEAU_COLORS.values())
    for j, classifier in enumerate(classificationResult):
        data = df[df['classification'] == classifier]
        ax.eventplot(data.index, colors=colors[j], lineoffsets = [offset])

def plotLocation(df, type = 'plot'):

    fig, ax = plt.subplots(2, 1)
    if(type == 'scatter'):
        ax[0].scatter(df.index, df['latitude'], s = 1)
        ax0_2 = ax[0].twinx()
        ax0_2.scatter(df.index, df['longitude'], s = 1)
        ax[1].scatter(df['latitude'], df['longitude'], s = 1)
        return 0 ;

    ax[0].plot(df['latitude'])
    ax0_2 = ax[0].twinx()
    ax0_2.plot(df['longitude'])
    ax[1].plot(df['latitude'], df['longitude'])

def plotScatter(df):
    setOfClassifiers = util.getSetOfItem(df['classification'])
    fig, ax = plt.subplots()
    for i, classifier in enumerate(setOfClassifiers):
        ax.scatter(df[df['classification'] == classifier]['latitude'], df[df['classification'] == classifier]['longitude'], label = classifier)
    plt.legend()