import os
import sys

import pandas as pd
import numpy as np

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USvisaData

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:     
            raise USvisaException(e, sys) from e
        
    def export_data_into_feature_store(self) -> DataFrame:
            """
            Method Name : export_data_into_feature_store
            Description : This method exports data from mongodb to csv file
            
            Output      : A csv file is created in feature store folder
            On Failure  : Raise Exception
            """
            try:
                logging.info(f"Exporting data from mongodb to feature store folder")
                usvisa_data  = USvisaData()
                dataframe = usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
                logging.info(f"Shape of Dataframe: {dataframe.shape}")
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path
                dir_path = os.path.dirname(feature_store_file_path)
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Exporting dataframe to feature store folder: {feature_store_file_path}")
                dataframe.to_csv(feature_store_file_path, index=False, header=True)
                return dataframe
            
            except Exception as e:
                raise USvisaException(e, sys) from e
            
    def split_data_as_train_test(self, dataframe:DataFrame) -> DataIngestionArtifact:
            """
            Method Name : split_data_as_train_test
            Description : This method splits the data into train and test file
            
            Output      : A csv file is created in ingested folder
            On Failure  : Raise Exception
            """
            try:
                train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
                logging.info(f"Performed train test split with test size: {self.data_ingestion_config.train_test_split_ratio}")
                logging.info(f"Exited split_data_as_train_test method of DataIngestion class")

                dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
                os.makedirs(dir_path, exist_ok=True)

                logging.info(f"Exporting training and testing dataframe to ingested folder")
                train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
                test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

                logging.info(f"Exported training and testing dataframe to ingested folder")

            except Exception as e:
                raise USvisaException(e, sys) from e
            
    def initiate_data_ingestion(self) ->DataIngestionArtifact:
            """

            Method Name :   initiate_data_ingestion
            Description :   This method initiates the data ingestion components of training pipeline 
            
            Output      :   train set and test set are returned as the artifacts of data ingestion components
            On Failure  :   Write an exception log and then raise an exception
            """
            logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

            try:
                dataframe = self.export_data_into_feature_store()

                logging.info("Got the data from mongodb")

                self.split_data_as_train_test(dataframe)

                logging.info("Performed train test split on the dataset")

                logging.info(
                    "Exited initiate_data_ingestion method of Data_Ingestion class"
                )

                data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)
                
                logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
                return data_ingestion_artifact
            except Exception as e:
                raise USvisaException(e, sys) from e


                

        