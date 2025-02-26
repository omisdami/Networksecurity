from Networksecurity.Entity.artifact_entitiy import DataIngestionArtifact,DataValidationArtifact
from Networksecurity.Entity.config_entity import DataValidationConfig
from Networksecurity.exception.exception import NetworkSecurityException 
from Networksecurity.logging.logger import logger
from Networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from Networksecurity.utils.Main_utils.utils import read_yaml_file,write_yaml_file 


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logger.info(f"Required number of columns:{number_of_columns}")
            logger.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def check_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = dataframe.select_dtypes(include=['number']).columns
            if len(numerical_columns) > 0:
                logger.info(f"Numerical columns found: {list(numerical_columns)}")
                return True
            logger.info("No numerical columns found in the dataset.")
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe=self.read_data(train_file_path)
            test_dataframe=self.read_data(test_file_path)
            

            error_messages= []

            # Validate number of columns
            if not self.validate_number_of_columns(train_dataframe):
                error_messages.append("Train dataframe does not contain all required columns.")
            if not self.validate_number_of_columns(test_dataframe):
                error_messages.append("Test dataframe does not contain all required columns.")

            # Check if numerical columns exist
            if not self.check_numerical_columns_exist(train_dataframe):
                error_messages.append("Train dataframe does not contain numerical columns.")
            if not self.check_numerical_columns_exist(test_dataframe):
                error_messages.append("Test dataframe does not contain numerical columns.")

            # If any validation errors occurred, log and raise an exception
            if error_messages:
                full_error_message = "\n".join(error_messages)
                logger.error(full_error_message)
                

            ## detect drift
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)