from houseprice.logging.logger import logging
from houseprice.exception.exception import HousePriceException

from houseprice.entity.config_entity import ModelTrainerConfig
from houseprice.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from houseprice.constants import MODELS, MODEL_PARAMETERS

from houseprice.utils.main_utils.utils import load_numpy_array,save_object
from houseprice.utils.ml_utils.metrics.classification_metrics import get_regression_scores
from sklearn.metrics import r2_score

from sklearn.model_selection import GridSearchCV


import sys
import numpy as np
import pandas as pd


class ModelTrainer:
    def __init__(self,model_trainer_config,data_transformation_artifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise HousePriceException(e,sys)    

    @staticmethod
    def read_data(file_path):
        try:
            return load_numpy_array(file_path)
        except Exception as e:
            raise HousePriceException(e,sys)

    def model_train(self,X_train,y_train):
        try:
            ml_models = MODELS
            model_params = MODEL_PARAMETERS
            models = {}
            for model_name,model in ml_models.items():
                gs = GridSearchCV(model,model_params[model_name],cv = 3)
                gs.fit(X_train,y_train)

                models[model_name] = gs.best_estimator_

            return models

        except Exception as e:
            raise HousePriceException(e,sys)

    def model_evaluation(self,X_test,y_test,models:dict):
        try:
            report = {}
            for model_name,model in models.items():
                y_pred = model.predict(X_test)
                score = r2_score(y_test,y_pred)

                report[model_name] = score

            return report    

        except Exception as e:
            raise HousePriceException(e,sys)

    def initiate_model_trainer(self):
        try:
            train_array = self.read_data(self.data_transformation_artifact.transformed_train_file_path)
            test_array = self.read_data(self.data_transformation_artifact.transformed_test_file_path)    

            X_train,y_train,X_test,y_test = (
                train_array[:, :-1],
                train_array[: , -1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = self.model_train(X_train,y_train)
            print("models are", models)
            model_report = self.model_evaluation(X_test,y_test,models)
            print("model report",model_report)

            print(model_report.values())

            max_score = max(model_report.values())
            best_model_name = list(model_report.keys())[list(model_report.values()).index(max_score)]
            best_model = models[best_model_name]

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            train_metrics = get_regression_scores(y_train,y_train_pred)
            test_metrics = get_regression_scores(y_test,y_test_pred)

            ## save best model
            save_object(self.model_trainer_config.trained_model_path,best_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_path = self.model_trainer_config.trained_model_path,
                    train_metric_artifact = train_metrics,
                    test_metric_artifact = test_metrics
                
            )

            return model_trainer_artifact


        except Exception as e:
            raise HousePriceException(e,sys)

