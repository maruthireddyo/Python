import logging,pprint,time,signal,sys,os
import json
import subprocess
from subprocess import Popen, PIPE
import datetime
import xml.etree.cElementTree as ET
import constants
import logging_praas
logger=logging_praas.initialize_pricing_log(__name__)
logger.setLevel(logging.DEBUG)
# from contextlib import contextmanager
# Create a custom logger
# @contextmanager
# print(type(pricing_utils))
from functools import wraps
# from time import time

def timing(function):
   @wraps(function)
   def wrap(*args, **kw):
      ts = time.time()
      result = function(*args, **kw)
      te = time.time()
      logger.info("{0} - execution time : {1}".format(function.__name__,te-ts))
      # print 'func:%r args:[%r, %r] took: %2.4f sec' % \
      # (function.__name__, args, kw, te-ts)
      return result
   return wrap
def signal_handler(signum, frame):
   # print('You pressed Ctrl+C! for '+ str(signum))
   logger.warn('Programme interrupted by signal {}'.format(signum))
   #raise TimeoutException()
   sys.exit(1)

def set_signals():
# $SIG{'KILL'} = "signal_handler";
# $SIG{'SIGINT'}  = "signal_handler";
# $SIG{'SIGTERM'} = "signal_handler";
# $SIG{'SIGQUIT'} = "signal_handler";
# $SIG{'SIGHUP'}  = "signal_handler";
# $SIG{'SIGALRM'} = "signal_alarm";
   # for sig_name in [sig for sig in dir(signal) if sig.startswith("SIG")]:
   for sig_name in ['SIGKILL','SIGINT','SIGTERM','SIGQUIT','SIGHUP','SIGALRM']:
      try:
         #Filter signals that cant be caught
         if sig_name == 'SIGKILL':
            continue
         if sig_name == 'SIGSTOP':
            continue
         if sig_name == 'SIG_DFL':
            continue
         signum = getattr(signal,sig_name)
         signal.signal(signum,signal_handler)
      except (OSError, RuntimeError,ValueError):
         logger.exception("Signal setting failed for {}".format(sig_name))
         sys.exit(1)
def get_enterprise_info(inputXML):
   '''This is extract customer information from XML is customer infor doesnt exist in custinfo tag '''
   enterprise_info_dict={}
   inputxml = ET.parse(inputXML).getroot()
   for zoneinfo in inputxml.findall('ZoneInfo'):
      if zoneinfo.attrib:
         if zoneinfo.find('operator-id') is not None:
            enterprise_info_dict['operator-id']=zoneinfo.findtext('operator-id')
         if zoneinfo.find('company-id') is not None:
            enterprise_info_dict['company-id']=zoneinfo.findtext('company-id')
         if zoneinfo.find('PriceGroup-id') is not None:
            enterprise_info_dict['PriceGroup-id']=zoneinfo.findtext('PriceGroup-id')
   return enterprise_info_dict
   
def get_custinfo(inputXML):
   logger.debug("Setting customer info based on data from input XMLs - {0} ".format(inputXML))
   inputxml = ET.parse(inputXML).getroot()
   custinfo_dict={}
   inputxml = ET.parse(inputXML).getroot()
   for custinfo in inputxml.findall('CustomerInfo'):
      if not custinfo.attrib:
         for custinfo_child in custinfo.findall('*'):
            print custinfo_child.tag,list(custinfo_child),len(list(custinfo_child))
            if len(list(custinfo_child)) == 0 : custinfo_dict[custinfo_child.tag]=custinfo_child.text
            if(custinfo_child.tag == 'Regions'):
               for region in custinfo.findall('Regions/Region'):
                  custinfo_dict.setdefault(custinfo_child.tag,[])
                  if region.text in constants.DCP_REGION_MAP :
                     custinfo_dict[custinfo_child.tag].append(constants.DCP_REGION_MAP[region.text])
                  else:
                     logger.error("unsupported region name '{0}' exist in XML ".format(region.text))
                     sys.exit(1)
   # print pprint.pformat(custinfo_dict)
   return(custinfo_dict)

def get_mccmnc(inputXML):

   logger.debug("Setting MCCMNC based on data from input XMLs - {0} ".format(inputXML))
   node_service_map={'DataZone':'Data','SMSZone':'SMS','TelcoZone':'Telco','SMSCZone':'SMSC'}
   mccmnc_dict={}
   inputxml = ET.parse(inputXML).getroot()
   for zoneinfo in inputxml.findall('ZoneInfo'):
      if zoneinfo.attrib or not zoneinfo.attrib:
         # print "Zone info attributes are ",zoneinfo.attrib
         for service_zone in zoneinfo.findall('OriginatingZone/*'):
            # print(service_zone)
            if service_zone.tag in ('DataZone','SMSZone','TelcoZone','SMSCZone'):
               mccmnc_dict.setdefault(node_service_map.get(service_zone.tag),{})
               # print "Data zone - ",service_zone.get('name')
               for mccmnc in service_zone.findall('MCCMNC'):
                  # print "MCCMNC - ",mccmnc.text
                  if service_zone.tag == 'TelcoZone':
                     mccmnc_dict[node_service_map.get(service_zone.tag)].setdefault('MCCMNC',{})
                     mccmnc_dict[node_service_map.get(service_zone.tag)]['MCCMNC'].setdefault(service_zone.get('name'),[])
                     mccmnc_dict[node_service_map.get(service_zone.tag)]['MCCMNC'][service_zone.get('name')].append(mccmnc.text)
                  else:
                     mccmnc_dict[node_service_map.get(service_zone.tag)].setdefault(service_zone.get('name'),[])
                     mccmnc_dict[node_service_map.get(service_zone.tag)][service_zone.get('name')].append(mccmnc.text)
                  # mccmnc_dict.append(mccmnc.text)
         for service_zone in zoneinfo.findall('DestinationZone/*'):
            # print(service_zone)
            if service_zone.tag in ('TelcoZone'):
               mccmnc_dict.setdefault(node_service_map.get(service_zone.tag),{})
               # print "Data zone - ",service_zone.get('name')
               for callingcode in service_zone.findall('CallingCode'):
                  # print "MCCMNC - ",mccmnc.text
                  mccmnc_dict[node_service_map.get(service_zone.tag)].setdefault('CallingCode',{})
                  mccmnc_dict[node_service_map.get(service_zone.tag)]['CallingCode'].setdefault(service_zone.get('name'),[])
                  mccmnc_dict[node_service_map.get(service_zone.tag)]['CallingCode'][service_zone.get('name')].append(callingcode.text)
                  # mccmnc_dict.append(mccmnc.text)

   # pp = pprint.PrettyPrinter(indent=3)
   # pprint.pprint(mccmnc_dict)
   #Add dummy MCCMNC like 9999,88888 as per service
   return(mccmnc_dict)

def read_config_file(config_file_name):
   with open(config_file_name, 'r') as f:
     config = json.load(f)
     return(config)
def run_sqlplus(login,pwd,db_name,sql):
   sqlplus_script='''
   WHENEVER SQLERROR EXIT 1
   WHENEVER OSERROR EXIT 2
   set heading off
   set echo off
   set feedback off
   set pagesize 0
   SET VERIFY OFF
   SET TRIMSPOOL ON
   SET LINESIZE 32000
   SET SQLPROMPT ''
   {sql_statement}
   exit;'''

   connection='{user}/{password}@{db}'.format(user=login, password=pwd,db=db_name)
   sqlplus_script=sqlplus_script.format(sql_statement=sql)
   logger.debug("SQLPLUS statement\n"+sqlplus_script)
   p = subprocess.Popen(['sqlplus','-S',connection],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   (stdout,stderr) = p.communicate(sqlplus_script.encode('utf-8'))
   stdout_lines = stdout.decode('utf-8').split("\n")

   if stderr is not ' ':
      logger.debug("SQLPLUS output\n"+stdout)
      return filter(None,stdout_lines)
   else:
      logger.debug("SQLPLUS error\n"+stderr)
      raise

def set_enterprise_sequence(inputXML):
   #SEQ NUMBER USAGE SHOULD BE MADE MINIMAL, HOW TO HANDLE IT ? MAKING ID FILE IS NOT GOOD IDEA UNLESS WE ARE USING PRICELIST
   #IF SEQUENCE NUMBER INVOLVES IN PP UPDATE IT SHOULD GO THROUGH AUTO PPA FLOW BEFORE DEPLOYING TO PRODUCTION
   sqlplus_output = run_sqlplus(constants.INF_ORA_LOGIN,constants.INF_ORA_PWD,constants.INF_ORA_DB,constants.DCP_IFW_SEQ_SQL.format(op_abr=constants.DCP_CUSTOMER_INFO['operator-abbr']))
   if len(sqlplus_output) == 1:
      enterprise_seq_id=sqlplus_output[0]
      if  constants.DCP_CUSTOMER_INFO.has_key('operator-id') :
         constants.DCP_ENTERPRISE_SEQ[constants.DCP_CUSTOMER_INFO['operator-id']]=sqlplus_output[0]
      if  constants.DCP_CUSTOMER_INFO.has_key('company-id')  :
         constants.DCP_ENTERPRISE_SEQ[constants.DCP_CUSTOMER_INFO['company-id']]=sqlplus_output[0]
   else:
      logger.error("Error while fetching IFW SEQ")
def get_db_info(inputXML):
   #Set global dictionaries from BRM DB
   db_info_dict={}
   #needs to be customized
   if {'Operator','CustomerNumber','Currency'} <= set(constants.INPUT_XML_CUSTOMER_INFO):   
      db_info_dict['operator-name']=constants.INPUT_XML_CUSTOMER_INFO['Operator']
      db_info_dict['company-id']=constants.INPUT_XML_CUSTOMER_INFO['CustomerNumber']
      db_info_dict['operator-id']=constants.INPUT_XML_CUSTOMER_INFO['CustomerNumber'][:2]+constants.DCP_OPERATOR_ID_SUFFIX
      db_info_dict['currency-id']=constants.INPUT_XML_CUSTOMER_INFO['Currency']
      db_info_dict['agreement-number']=constants.INPUT_XML_CUSTOMER_INFO['AgreementNumber']
   else:
      logger.error("'Operator','CustomerNumber','Currency' are mandatory for pricing configuration")
      sys.exit(1)
   
   sqlplus_output = run_sqlplus(constants.INF_ORA_LOGIN,constants.INF_ORA_PWD,constants.INF_ORA_DB,constants.DCP_INF_OP_ABR_SQL.format(op_name=db_info_dict['operator-name']))
   if len(sqlplus_output) == 1:
      # enterprise_seq_id=sqlplus_output[0]
      db_info_dict['operator-abbr']=sqlplus_output[0]
   else:
      logger.error("Error while fetching operator-abbr")

   sqlplus_output = run_sqlplus(constants.INF_ORA_LOGIN,constants.INF_ORA_PWD,constants.INF_ORA_DB,constants.DCP_INF_OP_GLID_SEQ_SQL.format(op_name=db_info_dict['operator-name']))
   if len(sqlplus_output) == 1:
      # enterprise_seq_id=sqlplus_output[0]
      db_info_dict['op-glid-seq']=sqlplus_output[0]
   else:
      logger.error("Error while fetching operator GLID sequence country")
   
   sqlplus_output = run_sqlplus(constants.IFW_ORA_LOGIN,constants.IFW_ORA_PWD,constants.IFW_ORA_DB,constants.DCP_IFW_CURRENCY_SQL.format(currency=db_info_dict['currency-id']))
   print sqlplus_output[0]
   if len(sqlplus_output) == 1 and  constants.SEPERATOR_SEMICOLON in sqlplus_output[0]:
      # enterprise_seq_id=sqlplus_output[0]
      # if SEPERATOR_SEMICOLON not in sqlplus_output: 
      db_info_dict['currency-name']=sqlplus_output[0].split(constants.SEPERATOR_SEMICOLON)[0]
      db_info_dict['resource-name']=sqlplus_output[0].split(constants.SEPERATOR_SEMICOLON)[1]
   else:
      logger.error("Error while fetching enterprise currency")

   sqlplus_output = run_sqlplus(constants.INF_ORA_LOGIN,constants.INF_ORA_PWD,constants.INF_ORA_DB,constants.DCP_INF_VAT_COUNTRY_SQL.format(op_name_lc=db_info_dict['operator-name'].lower()))
   if len(sqlplus_output) == 1:
      # enterprise_seq_id=sqlplus_output[0]
      db_info_dict['vat-country']=sqlplus_output[0]
   else:
      logger.error("Error while fetching VAT country")
   # sqlplus_output = run_sqlplus(constants.INF_ORA_LOGIN,constants.INF_ORA_PWD,constants.INF_ORA_DB,constants.DCP_INF_TAX_CODE_SQL.format(op_name_lc=db_info_dict['operator-name'].lower()))
   sqlplus_output = run_sqlplus(constants.INF_ORA_LOGIN,constants.INF_ORA_PWD,constants.INF_ORA_DB,constants.DCP_INF_TAX_CODE_SQL.format(op_name_lc=db_info_dict['operator-name'].lower()))
   # k for k in lst if 'ab' in k
   if 'VAT' in constants.INPUT_XML_CUSTOMER_INFO and constants.INPUT_XML_CUSTOMER_INFO['VAT'] is not None:
      db_info_dict['primary-vat']=constants.INPUT_XML_CUSTOMER_INFO['Country']+constants.SEPERATOR_UNDERSCORE+constants.INPUT_XML_CUSTOMER_INFO['VAT'].zfill(2)
      if db_info_dict['primary-vat'] not in sqlplus_output :
         logger.warning("Enterprise country : '{0}', Enterprise tax rate : {1}% combination invalid".format(constants.INPUT_XML_CUSTOMER_INFO['Country'],constants.INPUT_XML_CUSTOMER_INFO['VAT']))
         db_info_dict['primary-vat']=db_info_dict['vat-country']+constants.SEPERATOR_UNDERSCORE+constants.INPUT_XML_CUSTOMER_INFO['VAT'].zfill(2)
         if db_info_dict['primary-vat'] not in sqlplus_output :
            logger.error("Operator country : '{0}', Enterprise tax rate : {1}% combination invalid".format(db_info_dict['vat-country'],constants.INPUT_XML_CUSTOMER_INFO['VAT']))
            logger.error("Billing supported tax codes (COUNTRY_TAXRATE) - {0}".format(', '.join(sqlplus_output)))
            sys.exit(1)
         else:
            logger.info("Primary tax for configuration is '{0}'".format(db_info_dict['primary-vat']))

   if 'SecondaryVAT' in constants.INPUT_XML_CUSTOMER_INFO and constants.INPUT_XML_CUSTOMER_INFO['SecondaryVAT'] is not None:
      logger.debug("Secondary taxation exist for enterprise")
      db_info_dict['secondary-vat']=constants.INPUT_XML_CUSTOMER_INFO['Country']+constants.SEPERATOR_UNDERSCORE+constants.INPUT_XML_CUSTOMER_INFO['SecondaryVAT'].zfill(2)
      if db_info_dict['secondary-vat'] not in sqlplus_output :
         logger.warning("Enterprise country : '{0}', Enterprise secondary tax rate : {1}% combination invalid".format(constants.INPUT_XML_CUSTOMER_INFO['Country'],constants.INPUT_XML_CUSTOMER_INFO['SecondaryVAT']))
         db_info_dict['secondary-vat']=db_info_dict['vat-country']+constants.SEPERATOR_UNDERSCORE+constants.INPUT_XML_CUSTOMER_INFO['SecondaryVAT'].zfill(2)
         if db_info_dict['secondary-vat'] not in sqlplus_output :
            logger.error("Operator country : '{0}', Enterprise secondary tax rate : {1}% combination invalid".format(db_info_dict['vat-country'],constants.INPUT_XML_CUSTOMER_INFO['SecondaryVAT']))
            logger.error("Billing supported tax codes (COUNTRY_TAXRATE) - {0}".format(', '.join(sqlplus_output)))
            sys.exit(1)
         else:
            logger.info("Secondary tax for configuration is '{0}'".format(db_info_dict['secondary-vat']))

   #Getting GLID config type
   op_glid_prefix=db_info_dict['op-glid-seq']+'9'
   if constants.INPUT_XML_CUSTOMER_INFO['VAT'] is None:
      dummy_tax=db_info_dict['vat-country']+"_00"
   else:
      dummy_tax=db_info_dict['primary-vat']
   sqlplus_output = run_sqlplus(constants.IFW_ORA_LOGIN,constants.IFW_ORA_PWD,constants.IFW_ORA_DB,constants.DCP_IFW_GLID_SQL.format(op_glid_seq=db_info_dict['op-glid-seq'],op_glid_prefix=op_glid_prefix,prim_tax_code_dummy=dummy_tax))
   if len(sqlplus_output) == 1:
      # enterprise_seq_id=sqlplus_output[0]
      if len(sqlplus_output[0]) == 7:
         db_info_dict['glid-per-zone']=True
         logger.info("GLID per price group will be configured in pipeline")
         db_info_dict['glid-taxcode-seq']=sqlplus_output[0][-2:-1]
         
      elif len(sqlplus_output[0]) == 6:
         db_info_dict['glid-per-zone']=False
         db_info_dict['glid-taxcode-seq']=sqlplus_output[0][-2:-1].zfill(2)
   else:
      logger.error("Error while fetching GLID per price group identifying configuration in pipeline")
   
   if db_info_dict['glid-per-zone']:
      print "True"
      
   return db_info_dict


def get_planinfo(inputXML):
   #Set global dictionaries from BRM DB
   logger.debug("Setting MCCMNC based on data from input XMLs - {0} ".format(inputXML))
   node_service_map={'DataZone':'Data','SMSZone':'SMS','TelcoZone':'Telco','SMSCZone':'SMSC'}
   plan_info_dict={}
   inputxml = ET.parse(inputXML).getroot()
   plan_info_dict['company']=''.join(['C',constants.DCP_CUSTOMER_INFO['company-id']])
   plan_info_dict['subsidiary']=constants.SEPERATOR_UNDERSCORE.join([plan_info_dict['company'],constants.DCP_CUSTOMER_INFO['company-id']])
   plan_info_dict['contract']=constants.SEPERATOR_UNDERSCORE.join([plan_info_dict['subsidiary'],constants.DCP_CUSTOMER_INFO['agreement-number'],'SC_01'])
   plan_info_dict['contract-addon']=constants.SEPERATOR_UNDERSCORE.join([plan_info_dict['subsidiary'],constants.DCP_CUSTOMER_INFO['agreement-number'],'SC_02'])
   for pp in inputxml.findall('.//PriceProfile'):
      ppid=pp.get('id')
      plan_info_dict[ppid]=constants.SEPERATOR_UNDERSCORE.join([plan_info_dict['contract'],ppid])
   # print plan_info_dict
   for addon_service in inputxml.findall('.//AddOnServices/Service'):
      type=addon_service.get('type')
      # print "KKKKKKKK",type,"AAAAAA"
      # print plan_info_dict
      plan_info_dict[type]=constants.SEPERATOR_UNDERSCORE.join([plan_info_dict['contract'],type])   
   return plan_info_dict

def set_global_constants(inputXML):
	# cxn_set_zoneinfo();
	# cxn_set_custinfo();
	# cxn_get_db_values();
	# cxn_set_tax_values();
	# cxn_set_planinfo();
	# cxn_set_rateplan_values();
	# cxn_set_basic_rateplan_values();
	# cxn_set_smsc_acct_nums();
   logger.debug("Setting global variables based on data from input XMLs")
   #Set global dictionaries from XML
   constants.INPUT_XML_MCCMNC=get_mccmnc(inputXML)
   constants.INPUT_XML_CUSTOMER_INFO=get_custinfo(inputXML)
   constants.DCP_CUSTOMER_INFO=get_enterprise_info(inputXML)#For shared pricing if custinfo is not there
   # constants.DCP_CUSTOMER_INFO['operator-name']=constants.INPUT_XML_CUSTOMER_INFO['Operator']
   print constants.DCP_CUSTOMER_INFO

   constants.DCP_CUSTOMER_INFO.update(get_db_info(inputXML))
   constants.DCP_PLAN_INFO=get_planinfo(inputXML)
   print constants.DCP_PLAN_INFO
   # print get_db_info(inputXML)
   # exit()





   
   # if constants.INPUT_XML_CUSTOMER_INFO['VAT'] is None:
      # constants.INPUT_XML_CUSTOMER_INFO['VAT']
      # format(i, '02d')
   # print sqlplus_output
   # if len(sqlplus_output) == 0 and  constants.SEPERATOR_SEMICOLON in sqlplus_output[0]:
      # # enterprise_seq_id=sqlplus_output[0]
      # # if SEPERATOR_SEMICOLON not in sqlplus_output: 
      # constants.DCP_CUSTOMER_INFO['currency-name']=sqlplus_output[0].split(';')[0]
      # constants.DCP_CUSTOMER_INFO['resourse-name']=sqlplus_output[0].split(';')[1]
   # else:
      # logger.error("Error while fetching configured tax values for operator")

   logger.debug("INPUT_XML_CUSTOMER_INFO dictionary from input XML\n"+pprint.pformat(constants.INPUT_XML_CUSTOMER_INFO))
   logger.debug("INPUT_XML_MCCMNC dictionary from input XML\n"+pprint.pformat(constants.INPUT_XML_MCCMNC))
   logger.debug("DCP_CUSTOMER_INFO dictionary from input XML\n"+pprint.pformat(constants.DCP_CUSTOMER_INFO))
   logger.debug("DCP_PLAN_INFO dictionary from input XML\n"+pprint.pformat(constants.DCP_PLAN_INFO))
   print pprint.pformat(constants.DCP_CUSTOMER_INFO)

def set_data_directories():

   operator_data_path=constants.DCP_PRAAS_DATA_PATH+constants.DCP_CUSTOMER_INFO['operator-id']
   if not os.path.exists(constants.DCP_PRAAS_DATA_PATH):
      os.system('mkdir {dir_path}'.format(dir_path=constants.DCP_PRAAS_DATA_PATH))   
   if not os.path.exists(operator_data_path):
      os.system('mkdir {dir_path}'.format(dir_path=operator_data_path))
   if  constants.DCP_CUSTOMER_INFO.has_key('company-id')  :
      enterprise_data_path=operator_data_path+'/'+constants.DCP_CUSTOMER_INFO['company-id']
      if not os.path.exists(enterprise_data_path): os.system('mkdir {dir_path}'.format(dir_path=enterprise_data_path))
      enterprise_data_instance_path=enterprise_data_path+'/'+constants.INSTANCE_TIME_STAMP
      os.system('mkdir {dir_path}'.format(dir_path=enterprise_data_instance_path))
   else:
      operator_data_path_shared=operator_data_path+'/'+constants.DCP_CUSTOMER_INFO['operator-id']
      if not os.path.exists(operator_data_path_shared): os.system('mkdir {dir_path}'.format(dir_path=operator_data_path_shared))
      operator_data_shared_instance_path=operator_data_path_shared+'/'+constants.INSTANCE_TIME_STAMP
      os.system('mkdir {dir_path}'.format(dir_path=operator_data_shared_instance_path))