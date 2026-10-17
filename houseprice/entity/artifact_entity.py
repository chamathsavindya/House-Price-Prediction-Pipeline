from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    valid_status:bool
    valid_train_file_path:str
    valid_test_file_path: str
    invalid_train_file_path:str
    invalid_test_file_path: str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str


@dataclass
class RegressionMetricsArtifact:
    rmse:float
    mae:float
    r2_score:float

@dataclass
class ModelTrainerArtifact:        
    trained_model_path: str
    train_metric_artifact: RegressionMetricsArtifact
    test_metric_artifact: RegressionMetricsArtifact
