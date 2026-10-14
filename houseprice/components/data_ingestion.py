import pandas as pd
import sys
import os
from sklearn.model_selection import train_test_split

from houseprice.entity.config_entity import DataIngestionConfig
from houseprice.entity.artifact_entity import DataIngestionArtifact
from houseprice.exception.exception import HousePriceException
from houseprice.logging.logger import logging

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousePriceException(e,sys)

    def import_data(self):
        dataframe = pd.read_csv(self.data_ingestion_config.data_source_path)
        return dataframe

    def store_data_in_feature_store(self,dataframe:pd.DataFrame):
        feature_store_file_path = self.data_ingestion_config.feature_store_file_path
        dir_path = os.path.dirname(feature_store_file_path)

        os.makedirs(dir_path,exist_ok = True)
        dataframe.to_csv(feature_store_file_path, header=True, index =False)
        return dataframe

    def train_test_split(self,dataframe:pd.DataFrame):
        train_df,test_df = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
        logging.info("performed train test split")

        dir_path = os.path.dirname(self.data_ingestion_config.training_data_file_path)
        os.makedirs(dir_path,exist_ok = True)

        train_df.to_csv(self.data_ingestion_config.training_data_file_path, header=True, index =False)
        test_df.to_csv(self.data_ingestion_config.testing_data_file_path, header=True, index =False)
        logging.info("expoted ingested train and test data")




    def initialize_data_ingestion(self):
        try:
            dataframe = self.import_data()
            dataframe = self.store_data_in_feature_store(dataframe)
            self.train_test_split(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path = self.data_ingestion_config.training_data_file_path,
                test_file_path = self.data_ingestion_config.testing_data_file_path
            )

            return data_ingestion_artifact
        except Exception as e:
            raise HousePriceException(e,sys)    

