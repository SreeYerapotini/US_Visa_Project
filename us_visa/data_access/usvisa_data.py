from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import USvisaException
from us_visa.logger import logging   

import pandas as pd
import sys
from typing import Optional
import numpy as np


class USvisaData:
    """ 
    This class helps us to report entire mongoDB record as pandas dataframe
    """
    def __init__(self):
        """
        Docstring for __init__
        
        :param self: Description
        """

        try:
            self.mongo_client = MongoDBClient(database_name = DATABASE_NAME)
        except Exception as e:
            raise USvisaException(e,sys)
        
    def export_collection_as_dataframe(self, collection_name:str, database_name:Optional[str] = None) -> pd.DataFrame:
        """
        This function helps us to export entire collection as pandas dataframe
               
        """
        try:
            if database_name is None:
                database_name = DATABASE_NAME
            
            collection = self.mongo_client.get_collection(collection_name=collection_name, database_name=database_name)
            data = collection.find()
            df = pd.DataFrame(data)
            if "_id" in df.columns:
                df.drop("_id", axis=1, inplace=True)
            return df
        except Exception as e:
            raise USvisaException(e,sys)