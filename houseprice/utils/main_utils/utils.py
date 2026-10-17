import os
import sys
import pickle
import numpy as np
from houseprice.exception.exception import HousePriceException
from houseprice.logging.logger import logging

import yaml

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousePriceException(e,sys)

def write_yaml_file(file_path:str,content:object,replace:bool= False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok = True)   
        with open(file_path,"w") as file:
            yaml.dump(content,file)     
    except Exception as e:
        raise HousePriceException(e,sys)    

def save_numpy_array(file_path,object:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path,"wb") as file_obj:
            np.save(file_obj,object)
    except Exception as e:
        raise HousePriceException(e,sys)    

def load_numpy_array(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise HousePriceException(e,sys)            


def save_object(file_path,object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok = True)

        with open(file_path,"wb") as file_path:
            pickle.dump(object,file_path)

    except Exception as e:
        raise HousePriceException(e,sys)
