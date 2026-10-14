from datetime import datetime
import os
from houseprice import constants

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%H")
        self.pipeline_name = constants.PIPELINE_NAME
        self.artifact_dir_name = constants.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_dir_name,timestamp)
        self.timestamp : str=timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,constants.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,constants.DATA_INGESTION_FEATURE_STORE_DIR,constants.RAW_FILE_NAME)
        self.training_data_file_path = os.path.join(self.data_ingestion_dir,constants.DATA_INGESTION_INGESTED_DIR,constants.TRAIN_FILE_NAME)
        self.testing_data_file_path = os.path.join(self.data_ingestion_dir,constants.DATA_INGESTION_INGESTED_DIR,constants.TEST_FILE_NAME)
        self.train_test_split_ratio = constants.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.data_source_path = constants.DATA_SOURCE_PATH

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,constants.DATA_VALIDATION_DIR)
        self.data_validation_valid_dir = os.path.join(self.data_validation_dir,constants.DATA_VALIDATION_VALID_DIR)
        self.data_validation_invalid_dir = os.path.join(self.data_validation_dir,constants.DATA_VALIDATION_INVALID_DIR)
        self.data_validation_drift_report_dir = os.path.join(self.data_validation_dir,constants.DATA_VALIDATION_DRIFT_REPORT_DIR)
        self.data_validation_drift_report_file_name = os.path.join(self.data_validation_drift_report_dir,constants.DATA_VALIDATION_DRIFT_REPORT_FILR_NAME)
        self.data_validation_valid_train_file_path = os.path.join(self.data_validation_valid_dir,constants.TRAIN_FILE_NAME)
        self.data_validation_valid_test_file_path = os.path.join(self.data_validation_valid_dir,constants.TEST_FILE_NAME)
        self.data_validation_invalid_train_file_path = os.path.join(self.data_validation_invalid_dir,constants.TRAIN_FILE_NAME)
        self.data_validation_invalid_test_file_path = os.path.join(self.data_validation_invalid_dir,constants.TEST_FILE_NAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,constants.DATA_TRANSFORMATION_DIR)  
        self.data_transformation_transformed_data_dir = os.path.join(self.data_transformed_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR) 
        self.data_transformation_transformed_object_dir  = os.path.join(self.data_transformation_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)
        self.transformed_data_train_file_path = os.path.join(self.data_transformation_transformed_data_dir,constants.TRAIN_FILE_NAME.replace("csv","npy"))
        self.transformed_data_test_file_path = os.path.join(self.data_transformation_transformed_data_dir,constants.TEST_FILE_NAME.replace("csv","npy"))

class ModelTrainerConfig:
    def __init__(self):
        pass        

