from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder

def encoder_categories(x):
    onehot_encoder = OneHotEncoder(sparse=False)
    x = x.reshape(len(x),1)
    

def preprocess_data(
    train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Pre processes data for modeling. Receives train, val and test dataframes
    and returns numpy ndarrays of cleaned up dataframes with feature engineering
    already performed.

    Arguments:
        train_df : pd.DataFrame
        val_df : pd.DataFrame
        test_df : pd.DataFrame

    Returns:
        train : np.ndarrary
        val : np.ndarrary
        test : np.ndarrary
    """
    # Print shape of input data
    print("Input train data shape: ", train_df.shape)
    print("Input val data shape: ", val_df.shape)
    print("Input test data shape: ", test_df.shape, "\n")

    # Make a copy of the dataframes
    working_train_df = train_df.copy()
    working_val_df = val_df.copy()
    working_test_df = test_df.copy()

    # 1. Correct outliers/anomalous values in numerical
    # columns (`DAYS_EMPLOYED` column).
    working_train_df["DAYS_EMPLOYED"].replace({365243: np.nan}, inplace=True)
    working_val_df["DAYS_EMPLOYED"].replace({365243: np.nan}, inplace=True)
    working_test_df["DAYS_EMPLOYED"].replace({365243: np.nan}, inplace=True)
    dataframes = [working_train_df, working_val_df, working_test_df]

    # 2. TODO Encode string categorical features (dytpe `object`):
    #     - If the feature has 2 categories encode using binary encoding,
    #       please use `sklearn.preprocessing.OrdinalEncoder()`. Only 4 columns
    #       from the dataset should have 2 categories.
    #     - If it has more than 2 categories, use one-hot encoding, please use
    #       `sklearn.preprocessing.OneHotEncoder()`. 12 columns
    #       from the dataset should have more than 2 categories.
    # Take into account that:
    #   - You must apply this to the 3 DataFrames (working_train_df, working_val_df,
    #     working_test_df).
    #   - In order to prevent overfitting and avoid Data Leakage you must use only
    #     working_train_df DataFrame to fit the OrdinalEncoder and
    #     OneHotEncoder classes, then use the fitted models to transform all the
    #     datasets.
    for idx, df in enumerate(dataframes): 
        binariesColumns = df.select_dtypes('object').iloc[:,np.logical_and(df.select_dtypes('object').nunique().to_numpy() <= 2, df.select_dtypes('object').columns != 'NAME_CONTRACT_TYPE')]
        columnsNames = binariesColumns.columns
        binariesColumns = OrdinalEncoder().fit_transform(binariesColumns)  
        df[columnsNames] = binariesColumns
        
        categoricalColumns = df.select_dtypes('object').iloc[:, df.select_dtypes('object').columns.map(lambda x : x not in columnsNames)]
        categoricalColumnsNames = categoricalColumns.columns
        
        for nameColumn in categoricalColumns:
            print(f'namecolumn is {nameColumn}')
            one = OneHotEncoder(sparse_output=False)
            column = df[nameColumn]
            nameForList = [str(names) for names in list(column.unique())]
            print(f'nameFor{nameForList}')
            if 'nan' in nameForList:
                nameForList.remove('nan')
                nameForList.sort()
                #nameForList.append('nan')
                column = column.to_numpy().reshape(len(column),1)
                column_encoded = pd.DataFrame(one.fit_transform(column)[:,:-1], columns=nameForList)
            else:
                nameForList.sort()
                column = column.to_numpy().reshape(len(column),1)
                column_encoded = pd.DataFrame(one.fit_transform(column), columns=nameForList)
                
            df.drop(nameColumn, axis=1)
            df = pd.concat([df, column_encoded], axis=1)
        dataframes[idx] = df
        print(df.head())
        print(df.shape)
        break
            

        del(binariesColumns)
        del(columnsNames)


    print(dataframes[0].shape)

    # 3. TODO Impute values for all columns with missing data or, just all the columns.
    # Use median as imputing value. Please use sklearn.impute.SimpleImputer().
    # Again, take into account that:
    #   - You must apply this to the 3 DataFrames (working_train_df, working_val_df,
    #     working_test_df).
    #   - In order to prevent overfitting and avoid Data Leakage you must use only
    #     working_train_df DataFrame to fit the SimpleImputer and then use the fitted
    #     model to transform all the datasets.


    # 4. TODO Feature scaling with Min-Max scaler. Apply this to all the columns.
    # Please use sklearn.preprocessing.MinMaxScaler().
    # Again, take into account that:
    #   - You must apply this to the 3 DataFrames (working_train_df, working_val_df,
    #     working_test_df).
    #   - In order to prevent overfitting and avoid Data Leakage you must use only
    #     working_train_df DataFrame to fit the MinMaxScaler and then use the fitted
    #     model to transform all the datasets.


    return dataframes
