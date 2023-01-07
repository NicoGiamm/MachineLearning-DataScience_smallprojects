import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from pandas_datareader import data as web
import os

plt.rcParams['figure.figsize'] = (18, 10)
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['axes.grid'] = True


def forecast_reshape_X_y(data, window_size=20):

    """
    attributes:
        data = time series data
        window_size = time window to reshape data, after the reshape the data will have dim (data.shape[0] - window_size, window_size)

    how it works:
        reshape data with n columns with n = window_size
        return reshaped data
    """

    X = []
    y = []

    for i in range(window_size, data.shape[0]-1):
        X.append(data.values[i-window_size:i,0])
        y.append(data.values[i:i+1,0])

    X = np.asarray(X).astype('float32')
    y = np.asarray(y).astype('float32')

    return X, y

#######################################################################################################

def forecast_reshape_X(data, window_size=20):

    """
    attributes:
        data = time series data
        window_size = time window to reshape data, after the reshape the data will have dim (data.shape[0] - window_size, window_size)

    how it works:
        reshape data with n columns with n = window_size
        return reshaped data
    """

    X = []

    for i in range(window_size, data.shape[0]+1):
        X.append(data.values[i-window_size:i,0])

    X = np.asarray(X).astype('float32')

    return X

#######################################################################################################

def get_historical_data(years=4):

    """
    Get Unicredit data from the stooq website

    returns:
        Close stock prices of unicredit data from 4 yeas ago to today
    """

    #Set te data to fetch at 4 years before the actual date
    today = date.today()
    start_date = today - relativedelta(years=years)

    #Get data from stooq
    data = pd.DataFrame(web.DataReader('0RLS.UK', 'stooq', start_date))

    #Take only Close prices ordered by date
    close = data[['Close']]
    close = close.sort_index(ascending = True)

    return close

#######################################################################################################

def get_today_data(ticker, ws=20, days=30):

    """
    Get data of the last 30 days needed for the algorithm
    """

    today = date.today() - timedelta(days=days)
    data = pd.DataFrame(web.DataReader(ticker, 'stooq', today))
    close = data[['Close']]
    close = close.sort_index(ascending = True)
    close = close[-(ws+1):]

    return close

#######################################################################################################

def update_report(date, true, predicted, filename='weekly_report.csv'):

    """
    Create a report with true and predicted value
    """

    if (os.path.exists(filename) == False):

        new_row = {'date': date, 'true': true, 'predicted': predicted}
        report = pd.DataFrame(new_row, index=[0])
        report.to_csv(filename, index=False)

    else:

        report = pd.read_csv(filename)

        if (str(date) in list(report.date)):

            raise TypeError('Date already in the report')

        else:

            new_row = {'date': date, 'true': true, 'predicted': predicted}
            report = report.append(new_row, ignore_index=True)
            report.to_csv(filename, index=False)

    return

#######################################################################################################

def report_stats(report):

        '''
        evaluate the trading strategy starting from the prediction of a model and a real stock data
        returns nothing, just fancy graph with some statistics and gains (or losses)
        '''
        prediction = report.predicted.values
        true = report.true.values

        pred_diff = []
        true_diff = []

        for i in range(true.shape[0]-1):
            pred_diff.append(prediction[i+1] - prediction[i])
            true_diff.append(true[i+1] - true[i])

        sns.lineplot( pred_diff, label = 'predicted')
        sns.lineplot( true_diff, label = 'true')
        plt.xlabel('Time')
        plt.ylabel('Price derivative')
        plt.title('Test')
        plt.grid()
        plt.show()

        score = []
        start = 200
        total = 0
        tot = []
        perc = []

        for i in range(1, true.shape[0]-1):

            percentage = (abs(true[i] - true[i-1])/true[i-1])

            if ((pred_diff[i-1] < 0 and true_diff[i-1] < 0) or (pred_diff[i-1] >= 0 and true_diff[i-1] >= 0)):
                score.append(1)
                total += start*percentage
                perc.append(percentage*100)
            else:
                score.append(0)
                total -= start*percentage
                perc.append(-percentage*100)

            tot.append(total)

        tot = np.array(tot)
        sns.histplot(score, discrete=True)
        score = np.array(score)
        plt.title('Ratio of correct prediction up/down')
        print(np.count_nonzero(score)/score.shape[0])
        plt.show()

        perc = np.array(perc)
        print(perc.mean(), perc.std())
        plt.title('Distribution of returns')
        plt.xlabel('Daily percentage of return')
        sns.histplot(perc, kde = True)
        plt.show ()

        print(total)
        sns.lineplot(tot)
        plt.xlabel('Days')
        plt.ylabel('Balance')
        plt.title('Test Balance')
        plt.show()

        return

#######################################################################################################

class data_reshaper(BaseEstimator, TransformerMixin):

    """
    Reshape data for the convolutional neural network
    """

    def __init__(self, ws=20):
        self.ws = ws

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        X = X.reshape(X.shape[0],1,self.ws,1)
        return X
