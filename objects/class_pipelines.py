import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from numpy import logical_and
from typing import List

"""
    Create your own function to obtain the data
    transform it
"""
def get_split_of_categoricalColumns(df: pd.DataFrame) -> List[pd.DataFrame]:

    #get the binaries columns
    binariesColumns = df.select_dtypes('object').iloc[:, logical_and(df.select_dtypes('object').columns.map(lambda x: df[x][df[x] != 'XNA'].nunique() <= 2) , df.select_dtypes('object').columns != 'NAME_CONTRACT_TYPE')]
    
    #get the categorical columns
    categoricalColumns = df.select_dtypes('object').iloc[:, df.select_dtypes('object').columns.map(lambda x : x not in binariesColumns.columns)]

    return [binariesColumns, categoricalColumns]



class newClass(BaseEstimator, TransformerMixin):

    def get_split_of_categoricalColumns(self, df: pd.DataFrame) -> List[pd.DataFrame]:
        binariesColumns = df.select_dtypes('object').iloc[:, logical_and(df.select_dtypes('object').columns.map(lambda x: df[x][df[x] != 'XNA'].nunique() <= 2) , df.select_dtypes('object').columns != 'NAME_CONTRACT_TYPE')]
    
        categoricalColumns = df.select_dtypes('object').iloc[:, df.select_dtypes('object').columns.map(lambda x : x not in binariesColumns.columns)]
    
        return [binariesColumns, categoricalColumns]

    def __init__(self):
        #self.state = True if state == 'train' else False
        self.state = True
        
    def fit(self, X:pd.DataFrame, y=None) -> None:
        print(self.state)
        print("entre al new class fit")
        if self.state:
            self.state = not(self.state)
            binariesColumnsDf, categoricalColumnsDf = self.get_split_of_categoricalColumns(X)
            self.binariesNames = binariesColumnsDf.columns
            self.categoricalNames = categoricalColumnsDf.columns
            print('sali')

    def transform(self, df:pd.DataFrame, y=None) -> list[pd.DataFrame, pd.DataFrame]:
        print('entre al transform de new class')
        return [df[self.binariesNames], df[self.categoricalNames]]

    def fit_transform(self, X, y=None):
        print('i entered the ft method')
        self.fit(X)
        return self.transform(X)
        

"""
   object for transfor 
"""
#TransformerMixin
class Encoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        print("entre al init de encoder")
        print(self)
    
    def fit(self, X, y=None):
        print('entre al encoder fit')

    def transform(self, X, y=None):
        print('entre al encoder transform')
        print(f'type = {type(X)}')
        print(f'len = {len(X)}')
        print(X)
"""
    def fit_transform(self, X, y=None):
       print('entre al ftrans de enconder')
       """
