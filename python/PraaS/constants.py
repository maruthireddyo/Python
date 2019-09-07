import sys
import os
import datetime
# from pricing_utils import *
INFRANET_HOME=os.environ["INFRANET_HOME"]
DCP_PYTHON_LIB_PATH=INFRANET_HOME+'/lib/python/ppa'
DCP_PRICING_CONFIG_FILE=INFRANET_HOME+'/apps/dcp_pricing/dcp_pricing.conf'
DCP_OPERATOR_ONBOARDING_FILE=INFRANET_HOME+'/install/scripts/operator_onboarding.values'
DCP_PRICING_INPUT_DIR=INFRANET_HOME+'/apps/dcp_pricing/input'
DCP_PRICING_REJECT_DIR=INFRANET_HOME+'/apps/dcp_pricing/reject'
DCP_PRICING_PROCESSING_DIR=INFRANET_HOME+'/apps/dcp_pricing/processing'

DCP_PRAAS_LOG_PATH=INFRANET_HOME+'/log/PraaS/'
DCP_PRAAS_DATA_PATH=INFRANET_HOME+'/data/apps/PraaS/'

INSTANCE_TIME_STAMP=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# DCP_PRAAS_LOG={
# 'CRITICAL'	: 50,
# 'ERROR'	   : 40,
# 'WARNING'	: 30,
# 'INFO'	   : 20,
# 'DEBUG'	   : 10,
# 'NOTSET'	   : 0
# }

SEPERATOR_SEMICOLON=';';
SEPERATOR_UNDERSCORE='_';
DCP_OPERATOR_ID_SUFFIX='000001';
#Credentials
INF_ORA_LOGIN ="dev10";
INF_ORA_PWD ="dev10";
INF_ORA_DB ="BRM75DEV";
IFW_ORA_LOGIN = "ifw10";
IFW_ORA_PWD ="ifw10";
IFW_ORA_DB ="BRM75DEV";
IFW_APP_HOST_NAME ="brm2dldr01";
#SQLs used
DCP_IFW_SEQ_SQL="select to_char({op_abr}_IFW_ID_SEQ.nextval,'FM0000') from dual;"
DCP_IFW_CURRENCY_SQL="select  a.currency||';'||b.resource_name from ifw_currency a,ifw_resource b where a.currency=b.currency and a.currency_id='{currency}';"
DCP_INF_OP_ABR_SQL="select a.name from CONFIG_TAXS_T a where a.nexusinfo='{op_name}';"
DCP_INF_VAT_COUNTRY_SQL="SELECT CVT.canon_country FROM config_taxs_t CTT,config_vat_t CVT WHERE  CTT.obj_id0 = CVT.obj_id0 AND CTT.rec_id = CVT.rec_id2 AND Lower(CTT.nexusinfo) = '{op_name_lc}';"
DCP_INF_OP_GLID_SEQ_SQL="select trim(to_number(substr(account_no,0,length(account_no)-6))) from account_t where name='{op_name}';"
DCP_INF_TAX_CODE_SQL="SELECT tax_code FROM config_cxn_default_vals_taxs_t WHERE lower(name)='{op_name_lc}';";
DCP_IFW_GLID_SQL="SELECT Substr(glaccount, Length('{op_glid_seq}') + 1, Length(glaccount)) FROM   IFW_GLACCOUNT WHERE  GLACCOUNT LIKE '{op_glid_prefix}%' AND SUBSTR(GLACCOUNT,LENGTH('{op_glid_prefix}%'),1)<>'9' AND TAXCODE='{prim_tax_code_dummy}' AND ROWNUM = 1;"


# SELECT Substr(glaccount, Length('1' + 1, Length(glaccount)) FROM   IFW_GLACCOUNT WHERE  GLACCOUNT LIKE '19%' AND SUBSTR(GLACCOUNT,LENGTH('19%'),1)<>'9' AND TAXCODE='SE_25' AND ROWNUM = 1;

#Constnats derived from from input XML
INPUT_XML_MCCMNC={}
INPUT_XML_CUSTOMER_INFO={}
DCP_CUSTOMER_INFO={}
DCP_PLAN_INFO={}
DCP_ENTERPRISE_SEQ={}
DCP_STANDARD_INFO={}#include all custom names here
DCP_REGION_MAP ={
   'AB' : 'BELLMSISDNP001',
   'PE' : 'BELLMSISDNP002',
   'NS' : 'BELLMSISDNP003',
   'QC' : 'BELLMSISDNP004',
   'NB' : 'BELLMSISDNP005',
   'SK' : 'BELLMSISDNP006',
   'NL' : 'BELLMSISDNP007',
   'BC' : 'BELLMSISDNP008',
   'MB' : 'BELLMSISDNP009',
   'ON' : 'BELLMSISDNP010'
}

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

# def set_global_variable():
   # global script_name
   # global script_path
   # global pricing_config
   # global secret_key
   # global INSTANCE_TIME_STAMP
   # # global logger
   # try:
      # INSTANCE_TIME_STAMP=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
      # script_name=os.path.basename(__file__)[:-3]
      # script_path=os.getcwd()
      # pricing_config=read_config_file(DCP_PRICING_CONFIG_FILE)
      # secret_key=pricing_config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
      # # raise('WTF')
      # # gun =1+'0'
   # except Exception as e:
      # print "Inside the set_global_variable"
      # logger.error("Error in set")
      # raise