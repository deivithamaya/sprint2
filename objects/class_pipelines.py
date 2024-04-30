import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from numpy import logical_and
from typing import List
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

"""
    function to obtain the data transform it
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

    def get_list_of_names_for_DataFrame(self, df:pd.DataFrame, namesOfColumns)-> List[str]:
        print(namesOfColumns)
        listOfNames = []
        for name in namesOfColumns:
            uniques = df[name].unique()
            uniques = [str(x) for x in uniques]
            #if ''==name : uniques.append('XNA')
            if 'nan' in uniques:
                print(f'this columns has nan values {name}')
                uniques.remove('nan')
                uniques.sort()
                uniques.append('nan'+str(name))
            else:
                uniques.sort()
            listOfNames += uniques

        return listOfNames 


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
            se = pd.Series(['XNA' for x in range(len(self.binariesNames))], index=self.binariesNames)
            X[self.binariesNames] = X[self.binariesNames].append(se, ignore_index=True)
            print('bin')
            print(X[self.binariesNames].head())
            print('cate')
            print(X[self.categoricalNames].head())
            # get the parameters of OrdinalEncoder and OneHotEncoder
            self.ordinalEncoder = OrdinalEncoder().fit(X[self.binariesNames])
            self.listOfNamesDataFrame = self.get_list_of_names_for_DataFrame(X, self.categoricalNames)
            #print(self.listOfNamesDataFrame)
            self.oneHotEncoder = OneHotEncoder(sparse_output=False).fit(X[self.categoricalNames])



    def transform(self, df:pd.DataFrame, y=None) -> pd.DataFrame:
        #df.drop(self.categoricalNames, inplace=True)
        index = df.index
        df[self.binariesNames] = self.ordinalEncoder.transform(df[self.binariesNames])
        df = pd.concat([df, pd.DataFrame(self.oneHotEncoder.transform(df[self.categoricalNames]), columns=self.listOfNamesDataFrame, index=index)], axis=1)
        df.drop(self.categoricalNames, axis=1, inplace=True)
        return df
        #return [df[self.binariesNames], df[self.categoricalNames]]

    def fit_transform(self, X, y=None):
        print('i entered the ft method')
        self.fit(X)
        return self.transform(X)
        

"""
   object for transfor 
"""
#TransformerMixin
class Encoder(BaseEstimator, TransformerMixin):
    def binariEncoder(self, binariesColumns):
        pass

    def __init__(self, df:pd.DataFrame):
        print("entre al init de encoder")
        self.df = df
        print(self)
    
    def fit(self, X:List[pd.DataFrame],y=None):
        print('entre al encoder fit') 
        print(type(X))
        print(X)

    def transform(self, X, y=None):
        print('entre al encoder transform')
        print(f'type = {type(X)}')
        print(f'len = {len(X)}')
        print(X)
"""
    def fit_transform(self, X, y=None):
       print('entre al ftrans de enconder')
       """
