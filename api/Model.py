# import libraries
import joblib
import numpy as np
import pandas as pd
import datetime as dt

class Model:
    def __init__(self):
        self.store_path = '/app/data/processed_store_data.csv'
        self.columns_path = '/app/api/training_columns.txt'
        self.store_data = pd.read_csv(self.store_path)
        self.snippet = None
        self.model_path = '/app/model/compressed_rf_sales.pkl'
        self.model = joblib.load(self.model_path)
        self.features = None
        self.target = None

    def read_data(self, json_string):
        self.snippet = pd.DataFrame(json_string, index=[0])

    def prepare(self):
        print(self.snippet['Open'][0])
        if self.snippet['Open'][0]!=0:

            # Capture training columns
            self.exp_cols = []

            with open(self.columns_path, 'r') as columns_file:
                self.exp_cols = columns_file.read().split(',')
                self.exp_cols.remove('')

            # Ensure datatypes
            self.snippet['Store'] = self.snippet['Store'].astype(int)
            self.snippet['DayOfWeek'] = self.snippet['DayOfWeek'].astype(int)
            self.snippet['Date'] = self.snippet['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
            self.snippet['Sales'] = self.snippet['Sales'].astype(float)
            self.snippet['Customers'] = self.snippet['Customers'].astype(int)
            self.snippet['Open'] = self.snippet['Open'].astype(int)
            self.snippet['Promo'] = self.snippet['Promo'].astype(int)
            self.snippet['StateHoliday'] = self.snippet['StateHoliday'].astype(str)
            self.snippet['SchoolHoliday'] = self.snippet['SchoolHoliday'].astype(int)

            # get store data
            self.snippet = pd.merge(self.snippet, self.store_data, on='Store', how='left')

            self.snippet = pd.get_dummies(self.snippet, columns=['StateHoliday'])

            # Change datatypes of 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2SinceMonth', 'Promo2SinceYear'
            for column in ['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2SinceWeek', 'Promo2SinceYear']:
                self.snippet[column] = self.snippet[column].fillna(0)
                self.snippet[column] = self.snippet[column].astype(int).astype(str)

            self.snippet['CompetitionOpenSinceMonth'] = self.snippet['CompetitionOpenSinceMonth'].str.pad(width=2, side='left', fillchar='0')
            self.snippet['Promo2SinceWeek'] = self.snippet['Promo2SinceWeek'].str.pad(width=2, side='left', fillchar='0')

            self.snippet['CompetitionOpenSinceMonth'] = self.snippet['CompetitionOpenSinceMonth'].replace('00', '01')
            self.snippet['CompetitionOpenSinceYear'] = self.snippet['CompetitionOpenSinceYear'].replace('0', '1800')
            self.snippet['Promo2SinceWeek'] = self.snippet['Promo2SinceWeek'].replace('00', '01')
            self.snippet['Promo2SinceYear'] = self.snippet['Promo2SinceYear'].replace('0', '1800')

            self.snippet['CompetitionOpenSince'] = self.snippet['CompetitionOpenSinceMonth'] + '_' + self.snippet['CompetitionOpenSinceYear']
            self.snippet['CompetitionOpenSince'] = self.snippet['CompetitionOpenSince'].apply(lambda x: dt.datetime.strptime(x, '%m_%Y'))

            self.snippet['Promo2Since'] = self.snippet['Promo2SinceWeek'] + '_' + self.snippet['Promo2SinceYear'] + ' SUN'
            self.snippet['Promo2Since'] = self.snippet['Promo2Since'].apply(lambda x: dt.datetime.strptime(x, '%U_%Y %a'))

            self.snippet['DaysSinceCompetitionOpen'] = self.snippet.apply(lambda x: 0 if x['CompetitionOpenSince'].year<=dt.date(1800, 12, 31).year else (0 if (x['Date'] <= x['CompetitionOpenSince']) else (x['Date']-x['CompetitionOpenSince']).days), axis=1)
            self.snippet['DaysSincePromo2'] = self.snippet.apply(lambda x: 0 if x['Promo2Since'].year<=dt.date(1800, 12, 31).year else (0 if (x['Date'] <= x['Promo2Since']) else (x['Date']-x['Promo2Since']).days), axis=1)

            for column in self.exp_cols:
                if column not in self.snippet.columns:
                    self.snippet[column] = 0
            
            
            self.features = self.snippet.drop(['Store', 'Date', 'Sales', 'CompetitionOpenSinceMonth',  
                                            'CompetitionOpenSinceYear', 'Promo2SinceWeek', 
                                            'Promo2SinceYear', 'PromoInterval', 'CompetitionOpenSince',
                                            'Promo2Since', 'Unnamed: 0'], axis=1)

            self.target = self.snippet[['Sales']]

    def predict_sales(self):
        if self.features['Open'][0]==0:
            pred_sales = np.array([0])
        else:
            self.features = self.features.drop('Open', axis=1)
            pred_sales = self.model.predict(self.features)

        return pred_sales

        
        


    

    


    
