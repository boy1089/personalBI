import matplotlib.pyplot as plt


from sklearn.ensemble import IsolationForest


def detectAnomaly(df, model_columns):

    clf = IsolationForest(n_estimators=100, max_samples = 'auto',
                          contamination= float(.12), max_features=1.0,
                          bootstrap=False, n_jobs = -1, random_state = 42, verbose = 0)
    clf.fit(df[model_columns])

    pred = clf.predict(df[model_columns])
    df['anomaly'] = pred
    outliers = df.loc[df['anomaly'] == -1]

    return df, outliers


def plotAnomaly(df, outliers):
    if(len(df.columns)== 1):
        fig, ax = plt.subplots()
        ax.plot(df.index, df[df.columns[0]])
        ax.scatter(outliers.index, outliers[df.columns[0]], color = 'red')
        ax.set_ylabel(df.columns[0])

        return 0
    fig, ax = plt.subplots(len(df.columns), 1, sharex=True)
    for i, item in enumerate(df.columns):
        ax[i].plot(df.index, df[item])
        ax[i].scatter(outliers.index, outliers[item], color = 'red')
        ax[i].set_ylabel(item)
