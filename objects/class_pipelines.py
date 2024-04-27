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
    def __init__(self, state='train'):
        self.state = 1 if state == 'train' else 0
        
    def fit(self, df:pd.DataFrame) -> None:
        print(self.state)
        print("entreeeeeeeee")
        if self.state:
            self.state = not(self.state)
            binariesColumnsDf, categoricalColumnsDf = get_split_of_categoricalColumns(df)
            self.binariesNames = binariesColumnsDf.columns
            self.categoricalNames = categoricalColumnsDf.columns
            print('entre')

    def transform(self, df:pd.DataFrame) -> list[pd.DataFrame, pd.DataFrame]:
        return [df[self.binariesNames], df[self.categoricalNames]]

"""
   object for transfor 
"""

class Encoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        print(self)
    
    def fit(self):
        print('entre al fit')

    def transform(self, X):
        print(f'type = {type(x)}')
        print(f'len = {len(X)}')
        print(X)
