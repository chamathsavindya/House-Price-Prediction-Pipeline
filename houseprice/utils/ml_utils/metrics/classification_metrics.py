from houseprice.exception.exception import HousePriceException
from houseprice.entity.artifact_entity import RegressionMetricsArtifact

import numpy as np
from sklearn.metrics import mean_squared_error,mean_absolute_error, r2_score

import sys


def get_regression_scores(y_true,y_pred):
    try:
        rmse = np.sqrt(mean_squared_error(y_true,y_pred))
        mae = mean_absolute_error(y_true,y_pred)
        r2 = r2_score(y_true,y_pred)

        regression_metric = RegressionMetricsArtifact(
            rmse= rmse,
            mae= mae,
            r2_score = r2
        )

        return regression_metric
    except Exception as e:
        raise HousePriceException(e,sys)