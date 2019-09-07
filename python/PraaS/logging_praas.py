import logging
import os
import datetime
import constants
# from PraaS.constants import *
import subprocess
# from pricing.utils.pricing_constants import *

def initialize_pricing_log(module_name):

   logger = logging.getLogger(module_name)
   if not os.path.exists(constants.DCP_PRAAS_LOG_PATH):
      os.system('mkdir {log_path}'.format(log_path=constants.DCP_PRAAS_LOG_PATH))   
   process_file_name=constants.DCP_PRAAS_LOG_PATH+'/'+'PraaS_'+constants.INSTANCE_TIME_STAMP+'.log'
   # print logger,"Inside initialize_pricing_log -  ",module_name,"-",file_name 
   # file_name='dcp_pricing_test.log'
   # Create handlers
   c_handler = logging.StreamHandler()
   f_handler = logging.FileHandler(process_file_name)
   c_handler.setLevel(logging.INFO)
   f_handler.setLevel(logging.DEBUG)

   # Create formatters and add it to handlers
   c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
   # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   f_format = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(funcName)20s() - %(message)s')
   c_handler.setFormatter(c_format)
   f_handler.setFormatter(f_format)

   # Add handlers to the logger
   logger.addHandler(c_handler)
   logger.addHandler(f_handler)

   # logger.info('This is a warning')
   # logger.error('This is an error')
   return logger

def initialize_enterprise_log(module_name):

   logger = logging.getLogger(module_name)

   enterprise_log_path=constants.DCP_PRAAS_LOG_PATH+constants.INPUT_XML_CUST_CUSTOMER_INFO['operator-id']
   if not os.path.exists(enterprise_log_path):
      os.system('mkdir {log_path}'.format(log_path=enterprise_log_path))
   if  constants.INPUT_XML_CUST_CUSTOMER_INFO.has_key('company-id')  :
      process_file_name=enterprise_log_path+'/'+constants.INPUT_XML_CUST_CUSTOMER_INFO['company-id']+'_'+constants.INSTANCE_TIME_STAMP+'.log'
   else:
      process_file_name=enterprise_log_path+'/'+constants.INPUT_XML_CUST_CUSTOMER_INFO['operator-id']+'_'+constants.INSTANCE_TIME_STAMP+'.log'
   # print logger,"Inside initialize_pricing_log -  ",module_name,"-",file_name 
   # file_name='dcp_pricing_test.log'
   # Create handlers
   c_handler = logging.StreamHandler()
   f_handler = logging.FileHandler(process_file_name)
   c_handler.setLevel(logging.ERROR)
   f_handler.setLevel(logging.DEBUG)

   # Create formatters and add it to handlers
   c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
   # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   f_format = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(funcName)20s() - %(message)s')
   c_handler.setFormatter(c_format)
   f_handler.setFormatter(f_format)

   # Add handlers to the logger
   logger.addHandler(c_handler)
   logger.addHandler(f_handler)
   

      

   # logger.info('This is a warning')
   # logger.error('This is an error')
   return logger   