import pandas as pd
import numpy as np
import os,sys

from analysis.logger import logging
from analysis.exception import AnalysisException
from analysis.config import mongo_client

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        
        if "_id" in df.columns:
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise SensorException(e, sys)