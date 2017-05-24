import numpy,time,math
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from datetime import date

def baseline_model(cols=13):
	# create model
	model = Sequential()
	model.add(Dense(cols, input_dim=cols, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model
"""
Input: datetime object
Outout: features tuple
Usage: date_extractor("1/3/10")
"""
def date_extractor(date_str,
                   b = 48, # number of time bins per day
                   minutes_per_bin = int((24 / float(48)) * 60)):
    
    date_list = date_str.split('-')
    d_obj = date(int(date_list[0]),int(date_list[1]),int(date_list[2]))

    day_of_week = d_obj.weekday()
    #*** TODO     day_num = (day_of_week + time_num)/7.0
    day_num = (day_of_week)/7.0
    day_cos = math.cos(day_num * 2 * math.pi)
    day_sin = math.sin(day_num * 2 * math.pi)
    
    year = d_obj.year
    month = d_obj.month
    day = d_obj.day
    
    weekend = 0
    #check if it is the weekend
    if day_of_week in [5,6]:
        weekend = 1
       
    return (year, month, day, day_num, day_cos, day_sin, weekend)

raw = pd.read_csv("commits_noaa.csv")
derived = raw.committer_date.apply(lambda s: pd.Series(date_extractor(s)))

X1 = pd.DataFrame(raw.values[:,(3,4,5,6,7,8)])
X2 = pd.DataFrame(derived.values)
X = pd.concat([X1,X2] , axis=1).values
Y = raw.values[:,1]/1000

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# evaluate model with standardized dataset
estimator = KerasRegressor(build_fn=baseline_model, nb_epoch=100, batch_size=5, verbose=0)

# TODO *** more splits here
kfold = KFold(n_splits=5, random_state=seed)
