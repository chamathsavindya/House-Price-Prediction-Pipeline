from houseprice.exception.exception import HousePriceException
from houseprice.logging.logger import logging

from houseprice.entity.config_entity import DataValidationConfig
from houseprice.entity.artifact_entity import DataIngestionArtifact
from houseprice.entity.artifact_entity import DataValidationArtifact

from houseprice.utils.main_utils.utils import read_yaml_file,write_yaml_file
from houseprice.constants import DATA_SCHEMA_FILE_PATH

from scipy.stats import ks_2samp
import pandas as pd
import os,sys


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.__schema_config = read_yaml_file(DATA_SCHEMA_FILE_PATH)

        except Exception as e:
            raise HousePriceException(e,sys)    

    @staticmethod
    def read_data(file_path:str)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise HousePriceException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame):
        try:
            required_num_of_cols = len(self.__schema_config["columns"])

            if len(dataframe.columns) == required_num_of_cols:
                logging.info("data frame has requeired number of columns")
                return True
            else:
                logging.info("data frame does not has requeired number of columns")
                return False

        except Exception as e:
            raise HousePriceException(e,sys)

    def validate_column_names(self,dataframe):
        try:
            required_columns = self.__schema_config["columns"]
          

            if sorted(dataframe.columns) == sorted(list(required_columns[0].keys())):
                return True
            else:
                return False

        except Exception as e:
            raise HousePriceException(e,sys)    

    def ditect_data_drift(self,base_dataframe:pd.DataFrame,current_dataframe:pd.DataFrame,treshhold):
        try:
            status = True
            report = {}

            for column in base_dataframe.columns:
                d1 = base_dataframe[column]
                d2 = current_dataframe[column]

                is_same_dist = ks_2samp(d1,d2)

                if is_same_dist.pvalue >= treshhold:
                    is_found = False

                else:
                    is_found = True
                    status = False

                report.update(
                    {column:{"p_value":float(is_same_dist.pvalue),
                             "drift_status":is_found}
                     }
                )

                drift_report_file_path = self.data_validation_config.data_validation_drift_report_file_name
                dir_path = os.path.dirname(drift_report_file_path)
                os.makedirs(dir_path, exist_ok = True)

                write_yaml_file(file_path=drift_report_file_path,content=report)

                return status
        except Exception as e:
            raise HousePriceException(e,sys)    


    def initialize_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            train_column_number_status = self.validate_number_of_columns(train_dataframe)
            test_column_number_status = self.validate_number_of_columns(test_dataframe)

            train_column_name_status = self.validate_column_names(train_dataframe)
            test_column_name_status = self.validate_column_names(test_dataframe)

            data_drift_status = self.ditect_data_drift(base_dataframe = train_dataframe,current_dataframe=test_dataframe,treshhold=0.05)

            dir_path = os.path.dirname(self.data_validation_config.data_validation_valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)


            print(self.data_validation_config.data_validation_valid_train_file_path)
            train_dataframe.to_csv(self.data_validation_config.data_validation_valid_train_file_path, index = False,header= True)
            test_dataframe.to_csv(self.data_validation_config.data_validation_valid_test_file_path, index = False,header= True)

            data_validation_artifact = DataValidationArtifact(
                    valid_status = data_drift_status,
                    valid_train_file_path = self.data_validation_config.data_validation_valid_train_file_path,
                    valid_test_file_path = self.data_validation_config.data_validation_valid_test_file_path,
                    invalid_train_file_path = None,
                    invalid_test_file_path = None,
                    drift_report_file_path = self.data_validation_config.data_validation_drift_report_file_name
            )

            return data_validation_artifact


        except Exception as e:
            raise HousePriceException(e,sys)


if __name__ == "__main__":
    data_schema = read_yaml_file(DATA_SCHEMA_FILE_PATH)
    print(data_schema["columns"][0])

