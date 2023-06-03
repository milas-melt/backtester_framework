import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score, mean_absolute_percentage_error

def compute_monthly_data(path_to_file):
    df = pd.read_excel(path_to_file)
    df.dropna(inplace = True)
    df.columns = ['ds', 'y']
    
    df.set_index(df['ds'], inplace=True)
    df.index = pd.to_datetime(df.index)
    
    # Fill forward
    df_resampled = df.resample('m').ffill()
    df_resampled['ds'] = df_resampled.index

    # Clast 460 months (approx 70% to 71% of the dataset) --> dataset include 652 months, 17 days excluding the end date.
    num_months = df_resampled.shape[0]
    start_date = num_months - 456
    test_set = df_resampled.iloc[start_date:, :]
    test_set.columns = ['ds', 'y_test']
    train_set = df_resampled.iloc[:start_date, :]

    # Return the train and test sets
    return train_set, test_set

def model_evaluation(y_true, y_pred, MAPE_threshold):

    print(f'MSE : {mean_squared_error(y_true, y_pred)}')
    print(f'MAE is : {mean_absolute_error(y_true, y_pred)}')
    print(f'MAPE is : {mean_absolute_percentage_error(y_true,y_pred)}')
    print(f'R2 is : {r2_score(y_true, y_pred)}',end='\n')

    if mean_absolute_percentage_error(y_true,y_pred) > MAPE_threshold:
        
        print(f"WARNING: MAPE > {MAPE_threshold}")