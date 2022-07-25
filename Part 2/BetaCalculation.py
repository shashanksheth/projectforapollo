import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize

df = pd.read_excel('task2_stock_data.xlsx')

def calculateBeta (asofdate, window, frequency):
    #calculate start date based on file
    firstdate=df.iloc[0,0]
    
    #set period according to window entered
    if window=="1y":
        period=-1
    elif window=="2y":
        period=-2
    else:
        print("Incorrect window entered. Options are: '1y' or '2y'.")
        return
    
    try:
        windowstart = pd.to_datetime(asofdate) + pd.DateOffset(years=period)
    except:
        print("Incorrect asofdate entered. Please use the following format: 'YYYY-MM-DD'")
        return
    
    if firstdate > pd.to_datetime(asofdate) + pd.DateOffset(years=period):
        print (f"WARNING: The time between the first date in the file <{firstdate.strftime('%Y-%m-%d')}> and the given asofdate <{asofdate}> is less than the given window <{window}>. The calculation is therefore performed on a shorter window of returns.")
    
    #trim the dataframe by asofdate and period
    #sort so that the return calculation includes the latest returns
    window_df = df.loc[(df['date'] < asofdate) & (df['date'] >= windowstart)].sort_values(by='date', ascending=False)
    
    #set freq based on frequency entered
    if frequency=="daily":
        freq=1
    elif frequency=="weekly":
        freq=5
    elif frequency=="bi-weekly":
        freq=5*2
    elif frequency=="monthly":
        #assumption. 20.97 was the average days in a month in the given file
        freq=21
    elif frequency=="quarterly":
        #assumption. multiplied monthly by 4
        freq=21*4
    else:
        print("Incorrect frequency entered. Options are: 'daily','bi-weekly','monthly', or 'quarterly'.")
        return
        
    #trim the dataframe by frequency
    freq_window_df = window_df.iloc[::freq, :]
    
    #calculate returns, winsorize, and store in a dictionary
    freq_window_df.set_index("date", inplace=True)
    returns={}
    for column in freq_window_df:
        data = freq_window_df[column]
        log_returns = np.log(data/data.shift())
        log_returns_winsorized = winsorize(log_returns,limits=[0.05, 0.05])
        returns[column]=log_returns_winsorized[1:]
    
    #calculate covariances and store in a dictionary
    covariances={}
    for key in returns:
        covariances[key] = np.cov(returns[key],returns["SPY US Equity"],bias=True)[1][0]
    
    #calculate market variance
    market_variance=np.var(returns["SPY US Equity"])
    
    #calculate betas store in a dictionary. Rounded to 10 due to lost precision issues
    betas = {}
    for key in covariances:
        betas[key]=round((covariances[key]/market_variance),10)
    
    #return the result
    return betas

# checking to see if the result is identical to the linear regression method.
# I chose to calculate covariance and variance to:
# (1) better understand the calculation in-depth, and
# (2) my guess is that linear regression is slower and/or more memory intensive

# from sklearn.linear_model import LinearRegression

# X = returns['SPY US Equity'].reshape(-1, 1)
# Y = returns['CWEN US Equity'].reshape(-1, 1)
 
# lin_regr = LinearRegression()
# lin_regr.fit(X, Y)
 
# lin_regr.coef_[0, 0]
