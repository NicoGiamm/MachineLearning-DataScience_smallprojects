import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from pickle import load
from tensorflow.keras.models import load_model
from datetime import date
import sys
import os
sys.path.insert(1, './utils/')
from Functions import get_today_data, forecast_reshape_X, update_report

plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['axes.labelsize'] = 15

def main():
    
    #Load everything necessary
    scaler_y = load(open('./skobjects/scaler_y.pkl', 'rb'))
    transformer = load(open('./skobjects/transformer.pkl', 'rb'))
    model = load_model('./skobjects/model')
    
    #Get data of today and yesterday
    ticker = '0RLS.UK'
    close = get_today_data(ticker)
    
    #Transform today data
    unicredit_today = forecast_reshape_X(close)
    unicredit_today = transformer.transform(unicredit_today)
    
    #Predict next stock price
    pred = model.predict(unicredit_today)
    pred = scaler_y.inverse_transform(pred)
    sns.lineplot(pred)
    plt.show()
    
    #Write previous prdiction and today data into a report
    true = float(close.loc[date.today()].values)
    predicted = float(np.round(pred[0],3))
    update_report(date=date.today(), true=true, predicted=predicted)
    
main()