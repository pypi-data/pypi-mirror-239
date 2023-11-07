'''
Date         : 2023-10-25 14:17:09
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-11-06 17:20:34
LastEditors  : BDFD
Description  : 
FilePath     : \tempproj\supervised_classification\_regression.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
import execdata as exe
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingClassifier


def Car_Prediction_0601(para_list):
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
    X, y = exe.data_preprocessing.sep(df, target_variable)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.13, random_state=14)
    ohe = OneHotEncoder()
    ohe.fit(X[['name', 'company', 'fuel_type']])
    lr_tunning = LinearRegression()
    column_transformation = make_column_transformer((
        OneHotEncoder(categories=ohe.categories_), ['name', 'company', 'fuel_type']),
        remainder='passthrough')
    model = make_pipeline(column_transformation, lr_tunning)
    model.fit(X_train, y_train)
    df_sample_columns = ['name', 'company', 'year', 'kms_driven', 'fuel_type']
    test_sample = (pd.DataFrame(columns=df_sample_columns, data=np.array([para_list[0], para_list[1],
                                                                          para_list[2], para_list[3],
                                                                          para_list[4]]).reshape(1, 5)))
    result = (model.predict(test_sample))[0]
    return result


def Tele_Customer_Churn_0602(para_list):
    '''
        Tree Type Logistic Regression Model
        For Section6.Project01-Car-Price-Predictor
        Github_Project:'https://github.com/bdfd/Section6.Project02-Telco_Customer_Churning_Prediction'
    '''
    df_1 = pd.read_csv(
        'https://raw.githubusercontent.com/bdfd/Section6.Project02-Telco_Customer_Churning_Prediction/main/1.0%20dataset/S602_Mungged.csv',
        encoding='utf-8')
    df_2 = pd.read_csv(
        'https://raw.githubusercontent.com/bdfd/Section6.Project02-Telco_Customer_Churning_Prediction/main/1.0%20dataset/S602_Preprocessed.csv',
        encoding='utf-8')
    target_feature = 'Churn'

    # split the dataset and prepare for modeling prediction
    X, y = exe.data_preprocessing.sep(df_1, target_feature)
    st = SMOTEENN()
    X_st, y_st = st.fit_resample(X, y)
    # splitting the over sampling dataset
    X_train_sap, X_test_sap, y_train_sap, y_test_sap = train_test_split(
        X_st, y_st, test_size=0.2)
    # GradientBoostingClassifier
    gbc_tunning = GradientBoostingClassifier(learning_rate=0.3, loss='log_loss',
                                             max_depth=19, max_leaf_nodes=24, min_samples_leaf=15,
                                             min_samples_split=8, n_estimators=250)
    gbc_tunning.fit(X_train_sap, y_train_sap)

    # prepare for transformed incoming data
    desire_list = df_1.columns.tolist()
    del desire_list[-2:]
    # print(desire_list)
    df_sample = exe.data_preprocessing.column_not_drop(df_2, desire_list)
    sample_le = exe.data_preprocessing.fit_label_encode(
        df_sample, df_sample.columns)

    df_sample_columns = ['SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                         'OnlineSecurity', 'TechSupport', 'Contract',
                         'PaperlessBilling', 'PaymentMethod']
    test_sample = (pd.DataFrame(columns=df_sample_columns, data=np.array(
        [para_list[0], para_list[1], para_list[2], para_list[3],
         para_list[4], para_list[5], para_list[6], para_list[7],
         para_list[8]]).reshape(1, 9)))
    transformed_sample_df = exe.data_preprocessing.transform_label_encode(
        test_sample, test_sample.columns, sample_le)
    transformed_sample_df['MonthlyCharges'] = para_list[9]
    result = (gbc_tunning.predict(transformed_sample_df))[0]
    return result
