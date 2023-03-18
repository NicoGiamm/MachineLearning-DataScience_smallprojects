import numpy as np
import seaborn as sns
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

plt.rcParams['figure.figsize'] = (18, 10)
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['axes.grid'] = True


def forecast_split(data, window_size=30, dtp=1, test_days=30):
    """
    attributes:
        data = time series data
        window_size = time window to reshape data, after the reshape the data will have dim (data.shape[0] - window_size, window_size)
        dtp = days to predict, it means how many days you want to predict for each row of X
        test_days = number of rows of produced X_test
    
    how it works:
        reshape data with n columns with n = window_size and y in m columns with m = dtp
        split data in train and test
        return splitted reshaped data
    """
    X = []
    y_rolled = []
    y_true = []
    for i in range(window_size, data.shape[0]-1-dtp):
        y_true.append(data.values[i+1:i+1+dtp,0])
    
    
    data = data.rolling(5).mean().dropna()
    for i in range(window_size, data.shape[0]-1-dtp):
        X.append(data.values[i+1-window_size:i+1,0].tolist())
        y_rolled.append(data.values[i+1:i+1+dtp,0])
    #    X[-1] += (data.values[i+1-window_size:i+1,0] - data.values[i-window_size:i,0]).tolist()
        
    X = np.asarray(X).astype('float32')
    y_true = np.asarray(y_true).astype('float32')
    y_rolled = np.asarray(y_rolled).astype('float32')
        
    X_train = X[:-test_days,:]
    X_test = X[-test_days:,:]
    y_train = y_rolled[:-test_days]
    y_test = y_true[-test_days:]
        
    return X_train, X_test, y_train, y_test

###############################################################################

class Forecastsimulator():
    
    def __init__(self, model):
        """
        method call sequence:
            - train/train_cnn or retrain/retrain_cnn
            - predict
            - simulate
            
        """
        self.model = model
 
    ###############################################################################

    def train_nn(self, X_train, y_train, epochs=50, batch_size=32, verbose=2):
        """
        train the model
        """
        
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
        return self.model
 
    ###############################################################################

    def train(self, X_train, y_train):
        """
        train the model
        """
        
        self.model.fit(X_train, y_train)
        return self.model
 
    ###############################################################################

    def predict(self, X_test):
        
        prediction = self.model.predict(X_test)
        return prediction
 
    ###############################################################################
    
    def plot_prediction(self, prediction, y_test):
        
        plt.plot(prediction[:,-1], color = 'green', label = 'Predicted Price')
        plt.plot(y_test[:,0], color = 'red', label = 'Real Price')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        return
    
    ###############################################################################
       
    def retrain_nn(self, model, X_train, X_test, y_train, y_test, retrain_period=30):
        
        ''' 
        retrain the given keras model (neural networks) every given period
        returns the prediction
        '''
        
        self.model = model
        self.train_nn(X_train, y_train, verbose=0)
        prediction = np.empty(shape=(1,y_test.shape[1]))
        dim = X_test.shape[0]
        
        for i in range(dim):
            
            print(i)
            pred = self.predict(X_test[0:1])
            prediction = np.append(prediction, pred, axis=0)
            
            X_train = np.append(X_train[1:], X_test[0:1], axis=0)
            X_test = X_test[1:]
            y_train = np.append(y_train[1:], y_test[0:1], axis=0)
            y_test = y_test[1:]
            
            if ((i+1)%retrain_period == 0):
                self.model = model
                self.train_nn(X_train, y_train, verbose = 0, epochs=70)
                
        prediction = prediction[1:]
        return prediction
    
    ###############################################################################
    
    def retrain(self, model, X_train, X_test, y_train, y_test, retrain_period=30):
        
        ''' 
        retrain the given model of sklearn every given period
        returns the prediction 
        '''
        
        self.model = model
        self.train(X_train, y_train)
        prediction = np.empty(shape=(1,y_test.shape[1]))
        dim = X_test.shape[0]
        
        for i in range(dim):
            
            print(i)
            pred = self.predict(X_test[0:1])
            prediction = np.append(prediction, pred.reshape(-1,y_test.shape[1]), axis = 0)
            
            X_train = np.append(X_train[1:], X_test[0:1], axis=0)
            X_test = X_test[1:]
            y_train = np.append(y_train[1:], y_test[0:1], axis=0)
            y_test = y_test[1:]
            
            if ((i+1)%retrain_period == 0):
                self.model = model
                self.train(X_train, y_train)
        
        prediction = prediction[1:]
        return prediction
    
    ###############################################################################
            
    def simulate(self, prediction, y_test):
        
        '''
        evaluate a trading strategy starting from the prediction of a model and a real stock data
        returns nothing, just fancy graph with some statistics and gains (or losses)
        '''
        
        pred_diff = []
        true_diff = []

        for i in range(y_test.shape[0]-1):
            pred_diff.append(prediction[i+1,-1] - prediction[i,-1])
            true_diff.append(y_test[i+1,0] - y_test[i,0])

        sns.lineplot( pred_diff, label = 'predicted')
        sns.lineplot( true_diff, label = 'true')
        plt.xlabel('Time')
        plt.ylabel('Price derivative')
        plt.title('Test')
        plt.show()
        
        score = []
        start = 200
        total = 0
        tot = []
        perc = []

        for i in range(1, y_test.shape[0]-1):
            
            percentage = (abs(y_test[i,0] - y_test[i-1,0])/y_test[i-1,0])
            
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
        
            