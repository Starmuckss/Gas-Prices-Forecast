import pandas as pd
import numpy as np
#from fbprophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
from data_prep import DataPrep
import prophet

class Forecast:
    def init(self):
        data_prep = DataPrep()
        self.input_data = data_prep.run()

    def train_test_data_selection(self, data, periods):
        test = data[-periods:]
        train = data[:-periods]
        
        return train, test
    
    def prophet_fc(self):
        # Data prep
        prophet_data = pd.DataFrame()
        prophet_data['y'] = self.input_data['motorin']
        prophet_data['ds'] = self.input_data['Date']
        
        periods = 3

        prophet_train, prophet_test = self.train_test_data_selection(prophet_data,periods=periods)

        m = prophet(yearly_seasonality = True, seasonality_prior_scale=0.1)
        m.fit(prophet_train)
        future = m.make_future_dataframe(periods=periods)
        forecast = m.predict(future)