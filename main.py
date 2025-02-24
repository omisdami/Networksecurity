from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logger
from Networksecurity.Entity.config_entity import DataIngestionConfig
from Networksecurity.Entity.config_entity import TrainingPipelineConfig 

import sys 

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig()
        data_ingestion = DataIngestion()

        logger.info("Initiate Data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)