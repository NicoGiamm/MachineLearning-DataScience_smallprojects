import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def simulate(prediction_low, prediction_high, y_true):
        
        '''
        evaluate a trading strategy starting from the prediction of a model and a real stock data
        returns nothing, just fancy graph with some statistics and gains (or losses)
        '''
        
        pred_diff_low = []
        pred_diff_high = []
        true_diff = []

        for i in range(y_true.shape[0]-1):
            pred_diff_low.append(prediction_low[i+1,-1] - prediction_low[i,-1])
            pred_diff_high.append(prediction_high[i+1,-1] - prediction_high[i,-1])
            true_diff.append(y_true[i+1] - y_true[i])

        sns.lineplot( pred_diff_low, label = 'predicted low')
        sns.lineplot( pred_diff_high, label = 'predicted high')
        sns.lineplot( true_diff, label = 'true')
        plt.xlabel('Time')
        plt.ylabel('Price derivative')
        plt.title('Test')
        plt.show()
        
        score = []
        start = 100
        total = 0
        tot = []
        perc = []

        for i in range(1, y_true.shape[0]-1):
            
            percentage = (abs(y_true[i] - y_true[i-1])/y_true[i-1])
            
            #play only when but high and low are both positive or negative else don't play
            if((pred_diff_low[i-1] <= 0 and pred_diff_high[i-1] <= 0) or (pred_diff_low[i-1] > 0 and pred_diff_high[i-1] > 0)):
                if ((pred_diff_low[i-1] <= 0 and pred_diff_high[i-1] <= 0 and true_diff[i-1] <= 0) or (pred_diff_low[i-1] > 0 and pred_diff_high[i-1] > 0 and true_diff[i-1] > 0)):
                    score.append(1)
                    total += start*percentage
                    perc.append(percentage*100)
                    
                else:
                    score.append(0)
                    total -= start*percentage
                    perc.append(-percentage*100)
                
                tot.append(total-2.5)
            else:
                score.append(0.5)
                perc.append(0)
                tot.append(total)
                
            ##if (i%20) == 0:
            ##    start += 500   
        
        tot = np.array(tot)
        sns.histplot(score)
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