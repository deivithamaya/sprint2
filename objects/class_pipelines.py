import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from numpy import logical_and
from typing import List
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
import random
"""
    function to obtain the data transform it
"""
def get_split_of_categoricalColumns(df: pd.DataFrame) -> List[pd.DataFrame]:

    binariesColumns = df.select_dtypes('object').iloc[:, logical_and(df.select_dtypes('object').columns.map(lambda x: df[x][df[x] != 'XNA'].nunique() <= 2) , df.select_dtypes('object').columns != 'NAME_CONTRACT_TYPE')]
    categoricalColumns = df.select_dtypes('object').iloc[:, df.select_dtypes('object').columns.map(lambda x : x not in binariesColumns.columns)]

    return [binariesColumns, categoricalColumns]



class newClass(BaseEstimator, TransformerMixin):

    def get_split_of_categoricalColumns(self, df: pd.DataFrame) -> List[pd.DataFrame]:
        #binariesColumns = df.select_dtypes('object').iloc[:, logical_and(df.select_dtypes('object').columns.map(lambda x: df[x][df[x] != 'XNA'].nunique() <= 2) , df.select_dtypes('object').columns != 'NAME_CONTRACT_TYPE')]
        binariesColumns = df.select_dtypes('object').iloc[:, logical_and(df.select_dtypes('object').nunique().to_numpy() <=2, df.select_dtypes('object').columns != 'CODE_GENDER')]
        categoricalColumns = df.select_dtypes('object').iloc[:, df.select_dtypes('object').columns.map(lambda x : x not in binariesColumns.columns)]
    
        return [binariesColumns, categoricalColumns]

    def get_list_of_names_for_DataFrame(self, df:pd.DataFrame, namesOfColumns)-> List[str]:
        listOfNames = []
        for name in namesOfColumns:
            uniques = df[name].unique()
            uniques = [str(x) for x in uniques]
            if 'nan' in uniques:
                uniques.remove('nan')
                uniques.sort()
                uniques.append('nan'+str(name))
            else:
                uniques.sort()
            listOfNames += uniques

        return listOfNames 


    def __init__(self):
        self.state = True
        
    def fit(self, X:pd.DataFrame, y=None) -> None:
        if self.state:
            #self.state =not(self.state)a
            binariesColumnsDf, categoricalColumnsDf = self.get_split_of_categoricalColumns(X)
            self.binariesNames = binariesColumnsDf.columns
            self.categoricalNames = categoricalColumnsDf.columns
            se = pd.Series(['XNA' for x in range(len(self.binariesNames))], index=self.binariesNames)
            X[self.binariesNames] = X[self.binariesNames].append(se, ignore_index=True)
            X.iloc[random.randrange(0, len(X)), X.columns == 'CODE_GENDER'] = 'XNA'
            #print('x in fit')
            #print(X.shape)
            # get the parameters of OrdinalEncoder and OneHotEncoder
            self.ordinalEncoder = OrdinalEncoder().fit(X[self.binariesNames])
            self.listOfNamesDataFrame = self.get_list_of_names_for_DataFrame(X, self.categoricalNames)
            self.oneHotEncoder = OneHotEncoder(sparse_output=False).fit(X[self.categoricalNames])

        return self

    def transform(self, df:pd.DataFrame) -> pd.DataFrame:
        #print('transform in encoder')
        #print(df.shape)
        #print(df.head())
        #print('antes')
        index = df.index
        df[self.binariesNames] = self.ordinalEncoder.transform(df[self.binariesNames])
        df = pd.concat([df, pd.DataFrame(self.oneHotEncoder.transform(df[self.categoricalNames]), columns=self.listOfNamesDataFrame, index=index)], axis=1)
        #print('after')
        df.drop(self.categoricalNames, axis=1, inplace=True)
        #print(df.shape)
        return df
"""
    def fit_transform(self, X, y=None):
        print('i entered the ft method')
        self.fit(X)
        return self.transform(X)
        
"""
"""
   object for transfor 
"""
#TransformerMixin
class Imputer(BaseEstimator, TransformerMixin):
    
    def get_numerical_columns(self, df:pd.DataFrame):
        namesOfNumericColumns = df.select_dtypes('number').columns

    def binariEncoder(self, binariesColumns):
        pass

    def __init__(self):
        pass

    def fit(self, df:pd.DataFrame,y=None) -> None:
        self.names = df.columns
        self.simpleImputer = SimpleImputer(strategy='mean')
        self.simpleImputer.fit(df.values)
        return self

    def transform(self, df:pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame(self.simpleImputer.transform(df.values), columns=self.names)
        return df
"""
    def fit_transform(self, X, y=None):
       print('entre al ftrans de enconder')
       """
