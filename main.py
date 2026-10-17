from houseprice.components.data_ingestion import DataIngestion
from houseprice.components.data_validation import DataValidation
from houseprice.components.data_transformation import DataTransformation
from houseprice.components.model_trainer import ModelTrainer

from houseprice.entity.config_entity import TrainingPipelineConfig
from houseprice.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig)

data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
data_ingestion = DataIngestion(data_ingestion_config)
data_ingestion_artifact = data_ingestion.initialize_data_ingestion()
print(data_ingestion_artifact)

data_validation_config = DataValidationConfig(TrainingPipelineConfig())
data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
data_validation_artifact = data_validation.initialize_data_validation()
print(data_validation_artifact)

data_transformation_config = DataTransformationConfig(TrainingPipelineConfig())
data_transformation = DataTransformation(data_transformation_config,data_validation_artifact)
data_transformation_artifact = data_transformation.innitialize_data_transformartion()
print(data_transformation_artifact)

model_trainer_config = ModelTrainerConfig(TrainingPipelineConfig())
model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
model_trainer_artifact = model_trainer.initiate_model_trainer()
print(model_trainer_artifact)

