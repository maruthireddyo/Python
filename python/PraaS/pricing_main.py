#!/usr/bin/python
import sys,os,logging,signal,time,subprocess,shutil,pprint
from subprocess import Popen, PIPE
time.sleep(1)
import logging_praas
import utils
import constants

logger=logging_praas.initialize_pricing_log(__name__)
logger.setLevel(logging.DEBUG)

def main():
   try:
      node_service_map={'DataZone':'Data','SMSZone':'SMS','TelcoZone':'Telco','SMSCZone':'SMSC'}
      # pricing.utils.pricing_constants.set_global_variable()
      input_file_list = [input_file for input_file in os.listdir(constants.DCP_PRICING_INPUT_DIR) if os.path.isfile(os.path.join(constants.DCP_PRICING_INPUT_DIR, input_file))]
      if len(input_file_list) == 0 :
         logger.info("Input directory is empty")
         return
      shutil.copy2(constants.DCP_PRICING_INPUT_DIR+"/"+input_file_list[0],constants.DCP_PRICING_PROCESSING_DIR)
      utils.set_global_constants(constants.DCP_PRICING_PROCESSING_DIR+"/"+'PPA_Case1.xml')
      utils.set_enterprise_sequence(constants.DCP_PRICING_PROCESSING_DIR+"/"+'PPA_Case1.xml')
   except Exception as e:
      # shutil.move(constants.DCP_PRICING_INPUT_DIR+"/"+input_file_list[0],constants.DCP_PRICING_REJECT_DIR)
      logger.exception("Exception in main")

def pipeline_config():
   #we should create data directories before this
   utils.set_data_directories()
   import pipeline
   pipeline.main()
   
#Main programme
if __name__ == "__main__":
   logger.debug(os.path.basename(__file__)+" started as main programme")
   utils.set_signals()
   time.sleep(2)
   main()
# time.sleep(100)
# print logger
# logger.error("Maruthi")

# return
# break
# sys.path.append(os.environ["INFRANET_HOME"]+'/lib/python')

# print os.environ["PYTHONPATH"]
# from pricing.utils.pricing_constants import *
# time.sleep(1)
# # import pricing.utils.pricing_utils
# import pricing.pipeline.price_groups
# from lxml import etree#XML validator
# import xml.etree.cElementTree as ET
# logger = None

# start_time = time.time()
# time.sleep(1)
# print("--- %s seconds ---" % (time.time() - start_time))
# #Setting Global variables
# global script_name
# global script_path
# global pricing_config
# global secret_key
# # global logger
# global INSTANCE_TIME_STAMP
# INSTANCE_TIME_STAMP=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# logger = pricing.utils.pricing_utils.initialize_pricing_log(__name__)
# logger = logging.getLogger(__name__)

# def main():
   # try:
      # node_service_map={'DataZone':'Data','SMSZone':'SMS','TelcoZone':'Telco','SMSCZone':'SMSC'}
      # pricing.utils.pricing_constants.set_global_variable()
      # input_file_list = [input_file for input_file in os.listdir(DCP_PRICING_INPUT_DIR) if os.path.isfile(os.path.join(DCP_PRICING_INPUT_DIR, input_file))]
      
      # mccmnc=get_mccmnc(DCP_PRICING_PROCESSING_DIR+"/"+'shared_price_groups.xml')
      # logger.info("Maruthi")
      # print "+++++++++++++"
      # # pprint.pprint(mccmnc)
      # # for atype in inputxml.findall('ZoneInfo'):
         # # if not atype.attrib:
            # # print "Dictionary is empty",atype.attrib
         # # print "maruthi 1"
         # # # print 
         # # print(atype.tag)
         # # print(atype.find('OriginatingZone').findall('DataZone'))
         # # print(atype.find('OriginatingZone').find('DataZone').get('name'))
         # # if atype.get('ActionType') is None:
            # # print "Zone info attribute is empty",atype.get('Action')
         # # print "Zone info attribute is empty",atype.get('Action')
      # # for child in inputxml:
         # # print "maruthi 2"
         # # print(child.tag, child.attrib)
      # #shutil.copy2(DCP_PRICING_INPUT_DIR+"/"+input_file_list[0],DCP_PRICING_PROCESSING_DIR)
      # #shutil.copy2()
   # except IndexError:
      # logger.error("Input file processing error")
      # logger.exception("Input file list error")
      # # sys.exit(1)
   # except Exception as e:
     # # logger.error("Error occured in main")
      # # shutil.move(DCP_PRICING_INPUT_DIR+"/"+input_file_list[0],DCP_PRICING_REJECT_DIR)
      # logger.error("erro in main")
      # logger.exception("Exception in main")
        # logging.exception("Exception handling")
        # print "Inside main block - trace\n",traceback.extract_stack()
        # print ppa
    # else:
        # print "Inside main else block\n",traceback.extract_stack()
    # finally:
        # print "Inside main finally block"
        # logger.error('Inside main finally block')
   # exit(222);
   # pricing.pipeline.price_groups.main()
   # root = ET.parse('shared_price_groups.xml').getroot()
   # print "maruthi"
   # for atype in root.findall('ZoneInfo'):
      # print "maruthi 1"
      # print(atype.get('OriginatingZone'))
   # for child in root:
      # print(child.tag, child.attrib)
    

    # print sqlplus_script
   # sql="select POID_ID0 from account_t;"
    
    # foobar = '{foo}{bar}'.format(foo=foo, bar=bar)
    # "insert into {0}({1},{2},{3}) values ({4}, {5}, {6})".format('users','name','age','dna','suzan',1010,'nda')
    # sqlCommand = 'select count(*) from account_t;'
    # queryResult, errorMessage = runSqlQuery(sqlplus_script)
   # sqlplus_output = pricing.utils.pricing_utils.run_sqlplus('dev10','dev10','BRM75DEV',sql)

   # for line in sqlplus_output:
      # print(line)

    # xmltodict.parse("""
    # <?xml version="1.0" ?>
    # <person>
      # <name>john</name>
      # <age>20</age>
    # </person>""")

    # pipeline_log_file_name='OPERATOR_NAME_OptionalEnterpriseName_OptionalPPID.sql'
    # #Create sample tests from price group XML
    # with open(pipeline_log_file_name, "a") as pipeline_sql_file:
        # pipeline_sql_file.write("WHENEVER SQLERROR EXIT ROLLBACK\n")
        # generate_ifw_zonemodel=create_ifw_zonemodel_inserts()#variables#lists etc
        
        # for sql_insert_statement in generate_ifw_zonemodel:
            # pipeline_sql_file.write(sql_insert_statement)
        # pipeline_sql_file.write("COMMIT;\nEXIT;\n")

    # print INFRANET_HOME
    # print sys.argv[0][:-3]
    # print secret_key
    # print pricing_config
    # print script_name
    # print script_path

    # logging.error('This is a error')    


#Setting Global variables
# global script_name
# global script_path
# global pricing_config
# global secret_key
# global logger

# files = []
# print "file operatin"
# for x in range(2):
   # print "before "
   # logger = pricing.utils.pricing_utils.initialize_pricing_log(__name__)
   # logger.error('----------------')
   # print "after"
# logger.error('+++++++++++++++++++')
# logger = initialize_pricing_log(__name__)
# logger.warning('This is a main programme warning')
# def signal_handler(signum, frame):
   # print('You pressed Ctrl+C!')
   # print('Programme interrupted by signal',signal.getsignal(signum))
   # #raise TimeoutException()
   # sys.exit(0)
# main()
# signal.signal(signal.SIGINT, signal_handler)
# print('Press Ctrl+C')
# signal.alarm(2)
# signal.pause()
#time.sleep(5)

# print pricing_constants.INFRANET_HOME
# print sys.argv[0][:-3]
# print pricing_constants.secret_key
# print pricing_constants.pricing_config
# print pricing_constants.script_name
# print pricing_constants.script_path    
    


# log = logging.getLogger(__name__)
# log.setLevel('DEBUG')
# log.addHandler(ppa_log.MyHandler())

# log.debug('debug message') 
# log.info('info message')
# log.warning('warning message')
# log.error('error message')

# import yaml
# logging.config.fileConfig(fname='pricing_config.conf', disable_existing_loggers=False)
# logging.config.fileConfig(fname='pricing_config', disable_existing_loggers=False)
# logging.config.fileConfig(fname='pricing_config', disable_existing_loggers=False)

# Get the logger specified in the file
# logger = logging.getLogger(__name__)

# logger.debug('This is a debug message')

# with open('pricing_config.yaml', 'r') as f:
    # config = yaml.safe_load(f.read())
    # logging.config.dictConfig(config)

# logger = logging.getLogger(__name__)

# logger.debug('This is a debug message')




# logging.basicConfig(level=logging.DEBUG,filename='dcp_pricing_test.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
