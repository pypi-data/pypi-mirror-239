'''
Date         : 2023-10-25 14:17:09
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-10-25 14:43:33
LastEditors  : BDFD
Description  : 
FilePath     : \tempproj\supervise_classification.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
import pandas as pd
import execdata as exe
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline


def Car_Prediction():
    '''
        Linear Regression Model
        For Section6.Project01-Car-Price-Predictor
        Github_Project:'https://github.com/bdfd/Section6.Project01-Car-Price-Predictor'
    '''
    df = pd.read_csv(
        'https://raw.githubusercontent.com/bdfd/Section6.Project01-Car-Price-Predictor/Pickle-Demo/dataset/Car_Munging_Data.csv',
        encoding='utf-8')
    df = df.iloc[:, 1:]
    target_variable = 'Price'
    X, y = exe.sep(df, target_variable)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.13, random_state=14)
    ohe = OneHotEncoder()
    ohe.fit(X[['name', 'company', 'fuel_type']])
    model = LinearRegression()
    column_transformation = make_column_transformer((
        OneHotEncoder(categories=ohe.categories_), ['name', 'company', 'fuel_type']),
        remainder='passthrough')
    pipe = make_pipeline(column_transformation, model)
    pipe.fit(X_train, y_train)
    return pipe
