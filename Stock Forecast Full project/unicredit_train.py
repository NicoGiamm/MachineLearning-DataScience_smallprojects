import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from pickle import dump
import sys
sys.path.insert(1, './utils/')
from Functions import get_historical_data, forecast_reshape_X_y, data_reshaper
from unicredit_model import cnn_lstm


def main():
    
    #Get data from stooq website
    unicredit = get_historical_data()
    
    #Reshape data for the model 
    X, y = forecast_reshape_X_y(unicredit, window_size=20)
    
    #Model needs to reshape target
    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y)
    
    #save scaler for inverse transform the future predicted output
    dump(scaler_y, open('./skobjects/scaler_y.pkl', 'wb'))
    print('y scaler saved')
    
    #Build model transformers
    transformer = Pipeline(steps=[('scaler', StandardScaler()), 
                                  ('reshaper', data_reshaper()),
                                 ])
    
    #Transform data and save the transformer
    X = transformer.fit_transform(X)
    dump(transformer, open('./skobjects/transformer.pkl', 'wb'))
    print('transformer saved')
  
    #Train and save model                     
    model = cnn_lstm()
    model.fit(X, y_scaled, epochs=50, batch_size=50, verbose=2)
    model.save('./skobjects/model', save_format='h5')
    print('model saved')
                         
    return 0
    
main()    