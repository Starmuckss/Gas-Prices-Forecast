import pandas as pd 

class DataPrep:
    
    def init():
        pass

    def run(self, data_path):
        """ Read, Clean and Forward Fill operations are done here"""
        self.read_data(data_path)
        self.clean_data()
        self.forwardfill_data()
        return self.data

    def read_data(self, data_path):
        self.data = pd.read_csv(data_path)
        
        print(self.data)
    
    def clean_data(self):
        self.data.date = pd.to_datetime(self.data.date)
        
    def forwardfill_data(self):
        """ data is updated only when there is a price change, therefore we should fill the blanks"""
        min_date = self.data.date.min()
        max_date = self.data.date.max()
        
        date_range = pd.date_range(min_date, max_date)
        df_date_range = pd.DataFrame({'date': list(date_range)})

        merged = pd.merge(left=self.data, right=df_date_range, how="left", on=['date'])
        merged.ffill()

        self.data = merged.copy()