from Networksecurity.Entity.artifact_entitiy import DataIngestionArtifact,DataValidationArtifact
from Networksecurity.Entity.config_entity import DataValidationConfig
from Networksecurity.exception.exception import NetworkSecurityException 
from Networksecurity.logging.logger import logger
from scipy.stats import ks_2samp
import pandas as pd
import os,sys

