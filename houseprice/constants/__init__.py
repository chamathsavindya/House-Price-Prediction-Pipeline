import os
import numpy as np

TARGET_COL = ""
PIPELINE_NAME = "housepriceprediction"
ARTIFACT_DIR = "artifacts"

RAW_FILE_NAME = "data.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "tet.csv"
DATA_SOURCE_PATH = "data/housing.csv"

DATA_SCHEMA_FILE_PATH = "data_schema/schema.yml"

"""
Data Ingestion related constats start with 'DATA_INGESTION'
"""
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2

"""
Data validation related constats start with 'DATA_VALIDATION'
"""
DATA_VALIDATION_DIR = "data_validation"
DATA_VALIDATION_VALID_DRI = "valid"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yml"

"""
Data Transformation related constants starts with "DATA_TRANSFORMATION"
"""
DATA_TRANSFORMATION_DIR = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_objects"

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    
}