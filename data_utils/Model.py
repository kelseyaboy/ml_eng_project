# import libraries
import json
import joblib
import pandas as pd
import datetime as dt

class Model:
    def __init__(self):
        self.store_path = '../data/store.csv'
        self.store_data = pd.read_csv(self.store_path)
        self.snippet = None
        self.model_path = '../model/compressed_rf_sales.pkl'
        self.model = joblib.load(self.model_path)
        self.features = None
        self.target = None

    def read_data(self, json_string):
        self.snippet = pd.DataFrame(json_string, index=[0])

    def prepare(self):
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

        # Change datatypes of 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2SinceMonth', 'Promo2SinceYear'
        for column in ['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2SinceMonth', 'Promo2SinceYear']:
            self.snippet[column] = self.snippet[column].fillna(0)
            self.snippet[column] = self.snippet[column].astype(int).astype(str)

        self.snippet['CompetitionOpenSinceMonth'] = self.snippet['CompetitionOpenSinceMonth'].str.pad(width=2, side='left', fillchar='0')
        self.snippet['Promo2SinceWeek'] = self.snippet['Promo2SinceWeek'].str.pad(width=2, side='left', fillchar='0')

        self.snippet['CompetitionOpenSinceMonth'] = self.snippet['CompetitionOpenSinceMonth'].replace('00', '01')
        self.snippet['CompetitionOpenSinceYear'] = self.snippet['CompetitionOpenSinceYear'].replace('0', '1800')
        self.snippet['Promo2SinceWeek'] = self.snippet['Promo2SinceWeek'].replace('00', '01')
        self.snippet['Promo2SinceYear'] = self.snippet['Promo2SinceYear'].replace('0', '1800')

        self.snippet['CompetitionOpenSince'] = self.snippet['CompetitionOpenSinceMonth'] + '_' + store['CompetitionOpenSinceYear']
        self.snippet['CompetitionOpenSince'] = self.snippet['CompetitionOpenSince'].apply(lambda x: dt.datetime.strptime(x, '%m_%Y'))

        self.snippet['Promo2Since'] = self.snippet['Promo2SinceWeek'] + '_' + self.snippet['Promo2SinceYear'] + ' SUN'
        self.snippet['Promo2Since'] = self.snippet['Promo2Since'].apply(lambda x: dt.datetime.strptime(x, '%U_%Y %a'))

        self.snippet = pd.get_dummies(self.snippet, columns=['StateHoliday', 'StoreType', 'Assortment'])

        self.features = self.snippet[['DayOfWeek', 'Customers', 'Promo', 
                                      'StateHoliday', 'SchoolHoliday', 'StoreType', 
                                      'Assortment', 'CompetitionDistance', 'Promo2', 
                                      'DaysSinceCompetitionOpen', 'DaysSincePromo2']]

        self.target = self.snippet[['Sales']]

    def predict_sales(self):
        return self.model.predict(self.features)

        
        


    

    


    
