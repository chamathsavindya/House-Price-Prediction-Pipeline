from houseprice.components.data_ingestion import DataIngestion
from houseprice.entity.config_entity import TrainingPipelineConfig
from houseprice.entity.config_entity import DataIngestionConfig

data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
data_ingestion = DataIngestion(data_ingestion_config)
data_ingestion_artifact = data_ingestion.initialize_data_ingestion()
print(data_ingestion_artifact)