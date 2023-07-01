import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import yfinance as yf
import os

def forecast_reshape_X(data: np.ndarray, window_size: int=20):

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
        X.append(data[i-window_size:i,0])

    return X


def forecast_reshape_X_y(data: np.ndarray, window_size: int=20):

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
        X.append(data[i-window_size:i,0])
        y.append(data[i:i+1,0])

    return X, y

def get_data(ticker: str, period: str='7d', interval: str='1m'):

    """
    Get data from yahoo finance

    returns:
        Mean stock price in the specified period and interval
    """

    data = yf.download(tickers=ticker, period=period, interval=interval)

    #Compute the mean between hig and low
    data['Mean'] = (data['High'] + data['Low']) / 2

    return data[['Mean']]