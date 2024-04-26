import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from numpy import logical_and

"""
    Create your own function to obtain the data
    transform it
"""
def get_split_of_categoricalColumns(df: pd.DataFrame) -> List[binariesColumns:pd.Dataframe, categoricalColumns:pd.DataFrame]:

    #get the binaries columns
    binariesColumns = df.select_dtypes('object').iloc[:, logical_and(df.select_dtypes('object').columns.map(lambda x: df[x][df[x] != 'XNA'].nunique() <= 2) , df.select_dtypes('object').columns != 'NAME_CONTRACT_TYPE')]
    
    #get the categorical columns
    categoricalColumns = df.select_dtypes('object').iloc[:, df.select_dtypes('object').columns.map(lambda x : x not in binariesColumns.columns)]

    return [binariesColumns, categoricalColumns]



class newClass(BaseEstimator, TransformerMixin):
    def __init__(self, state='Train'):
        self.state = 1 if state == 'Train' else 0
        
    def fit(self, df:pd.DataFrame) -> None:
        if self.state:
            self.df = df
            binariesColumnsDf, categoricalColumnsDf = get_split_of_categoricalColumns(self.df)
            self.binariesNames = binariesColumnsDf.columns
            self.categoricalNames = categoricalColumnsDf.columns


    def transform(self) -> list[binariesColumns:pd.DataFrame, categoricalColumns:pd.DataFrame]:
        return [self.df[self.binariesNames], self.df[self.categoricalNames]

"""
   object for transfor 
"""

class Encoder(BaseEstimator, TransformerMixin):
    

