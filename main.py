from analysis.logger import logging
from analysis.exception import AnalysisException
from analysis.utils import get_collection_as_dataframe
from analysis.entity import config_entity
from analysis.components.data_ingestion import DataIngestion
import sys,os


print(__name__)
if __name__=="__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          #data ingestion
          data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
     except Exception as e:
        raise AnalysisException(e, sys)