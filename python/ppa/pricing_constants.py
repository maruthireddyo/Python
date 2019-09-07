import sys
import os
from pricing_utils import *
INFRANET_HOME=os.environ["INFRANET_HOME"]
DCP_PYTHON_LIB_PATH=INFRANET_HOME+'/lib/python/ppa'
DCP_PRICING_CONFIG_FILE=INFRANET_HOME+'/apps/cxn_pricing_test/Connexion/dcp_pricing_test.conf'

def set_global_variable():
	global script_name
	global script_path
	global pricing_config
	global secret_key
	# global logger	

	script_name=os.path.basename(__file__)[:-3]
	script_path=os.getcwd()
	pricing_config=read_config_file(DCP_PRICING_CONFIG_FILE)
	secret_key=pricing_config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
