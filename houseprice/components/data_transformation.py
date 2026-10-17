from houseprice.logging.logger import logging
from houseprice.exception.exception import HousePriceException

from houseprice.constants import TARGET_COL
from houseprice.constants import DATA_TRANSFORMATION_IMPUTER_PARAMS

from houseprice.utils.main_utils.utils import save_numpy_array,save_object

from houseprice.entity.artifact_entity import DataTransformationArtifact

from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

import pandas as pd
import sys
import numpy as np



class DataTransformation:
    def __init__(self,data_transformation_config,data_validation_artifact):
        self.data_transformation_config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact

    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise HousePriceException(e,sys)

    def get_data_transformer_object(self,numerical_column_names,categorical_column_names):
        try:
            numerical_pipeline = Pipeline(
                steps=[
                    ("knnimputer",KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)),
                    ("scaler",StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("simpleimputer",SimpleImputer(strategy="most_frequent")),
                    ("onehotencoder",OneHotEncoder(handle_unknown="ignore"))
                ]
            )

            preprocessor = ColumnTransformer(
                transformers = [
                    ("numerical_transformer",numerical_pipeline,numerical_column_names),
                    ("categorical_transformer",categorical_pipeline,categorical_column_names)
                ]
            )

            return preprocessor

            
        except Exception as e:
            raise HousePriceException(e,sys)

    def column_combination(self,dataframe):
        try:
            pass
        except Exception as e:
            raise HousePriceException(e,sys)    

    def innitialize_data_transformartion(self):
        try:
            train_dataframe = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_dataframe = self.read_data(self.data_validation_artifact.valid_test_file_path)

            ## split data into features and target
            train_features = train_dataframe.drop(columns=[TARGET_COL])
            train_target = train_dataframe[TARGET_COL]

            test_features = test_dataframe.drop(columns=[TARGET_COL])
            test_target = test_dataframe[TARGET_COL]

            ## define numerical and categorical column names
            numerical_column_names = train_features.select_dtypes(include=[np.number]).columns.to_list()
            categorical_column_names = train_features.select_dtypes(include="object").columns.to_list()


            ## get data transformer object
            transformer = self.get_data_transformer_object(numerical_column_names = numerical_column_names,categorical_column_names = categorical_column_names)

            ## transform train data
            transformed_train_features = transformer.fit_transform(train_features)

            ## transform test data
            transformed_test_features = transformer.transform(test_features)

            ## combine features and target
            train_array = np.c_[transformed_train_features,np.array(train_target)]
            test_array = np.c_[transformed_test_features,np.array(test_target)]


            ## save transformed data
            save_numpy_array(self.data_transformation_config.transformed_data_train_file_path,train_array)
            save_numpy_array(self.data_transformation_config.transformed_data_test_file_path,test_array)
            
            ## save data transformer object for later use
            save_object(self.data_transformation_config.data_transformation_transformed_object_dir,transformer)

            ## prepare data transformation artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path= self.data_transformation_config.transformed_data_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_data_test_file_path,
                transformed_object_file_path= self.data_transformation_config.data_transformation_transformed_object_dir,
            )
            ## return data transformation artifact
            return data_transformation_artifact
        
        except Exception as e:
            raise HousePriceException(e,sys)    
