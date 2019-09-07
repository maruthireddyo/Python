import sys
import os
from pricing_utils import *
INFRANET_HOME=os.environ["INFRANET_HOME"]
DCP_PYTHON_LIB_PATH=INFRANET_HOME+'/lib/python/ppa'
DCP_PRICING_CONFIG_FILE=INFRANET_HOME+'/apps/dcp_pricing/dcp_pricing.conf'
DCP_OPERATOR_ONBOARDING_FILE=INFRANET_HOME+'/install/scripts/operator_onboarding.values'
DCP_PRICING_INPUT_DIR=INFRANET_HOME+'/apps/dcp_pricing/input'
DCP_PRICING_REJECT_DIR=INFRANET_HOME+'/apps/dcp_pricing/reject'
DCP_PRICING_PROCESSING_DIR=INFRANET_HOME+'/apps/dcp_pricing/processing'
# logger = initialize_pricing_log(__name__)
# def set_global_variable():
    # global script_name
    # global script_path
    # global pricing_config
    # global secret_key
    # # global logger    
    # try:
        # script_name=os.path.basename(__file__)[:-3]
        # script_path=os.getcwd()
        # pricing_config=read_config_file(DCP_PRICING_CONFIG_FILE)
        # secret_key=pricing_config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
        # # gun =1+'0'
        # # raise(Exception('spam', 'eggs'))    
    # except Exception as e:
        # print "Inside exception block\n",e
        # raise Exception(e)
        # # raise "Inside exception block\n",e
        # # print ppa
    # else:
        # print "Inside else block\n",traceback.print_exc()
        # raise "Inside else block\n",traceback.print_exc()
    # finally:
        # print "Inside finally block\n"
        # raise "Inside finally block\n"
    # # exit()

def set_global_variable():
   global script_name
   global script_path
   global pricing_config
   global secret_key
   global INSTANCE_TIME_STAMP
   # global logger
   try:
      INSTANCE_TIME_STAMP=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
      script_name=os.path.basename(__file__)[:-3]
      script_path=os.getcwd()
      pricing_config=read_config_file(DCP_PRICING_CONFIG_FILE)
      secret_key=pricing_config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
      # raise('WTF')
      # gun =1+'0'
   except Exception as e:
      print "Inside the set_global_variable"
      logger.error("Error in set")
      raise