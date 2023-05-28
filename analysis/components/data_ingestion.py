from analysis.logger import logging
from analysis.exception import AnalysisException
from analysis.entity import artifact_entity
from analysis.entity import config_entity
from analysis import utils

import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise AnalysisException(e,sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame =utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
            )
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            logging.info("Save data in feature store")

            #Save data in feature store
            logging.info("Create feature store folder if not available")

            logging.info("create dataset directory folder if not available")
            #create dataset directory folder if not available
            feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_path)

            logging.info("Save df to feature store folder")
            #Save df to feature store folde
            os.makedirs(feature_store_dir,exist_ok=True)


            
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info("split dataset into train and test set")
            #split dataset into train and test set
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size)


            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

          
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            #Prepare artifact
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            return data_ingestion_artifact

        except Exception as e:
            raise AnalysisException(error_message=e, error_detail=sys)