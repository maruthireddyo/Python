#This module is to create all the required configuration in pipeline database
#Class constants
import sys,logging,pprint
import logging_praas
import constants
import utils
logger=logging_praas.initialize_pricing_log(__name__)
logger.setLevel(logging.DEBUG)

enterprise_logger=logging_praas.initialize_enterprise_log(__name__)
enterprise_logger.setLevel(logging.DEBUG)

#this should be called only after enterprise no/Operator Number is picked
logger.info("PriceGroup creation process initiated with time stamp {0}".format(constants.INSTANCE_TIME_STAMP))
enterprise_logger.info("PriceGroup creation process initiated with time stamp {0}".format(constants.INSTANCE_TIME_STAMP))

#Define global variables 
#Zone model is one for enterprise, there can be shared enterprises at operator level
#Naming needs to be defined accordingly
global ZONE_MODEL_NAME
global RATE_PLAN_NAME

def set_zone_model_name():
   global ZONE_MODEL_NAME
   custom_name_list=[]
   if constants.INPUT_XML_CUST_CUSTOMER_INFO.has_key('operator-abbr') : 
      custom_name_list.append(constants.INPUT_XML_CUST_CUSTOMER_INFO['operator-abbr'])
   if constants.INPUT_XML_CUST_CUSTOMER_INFO.has_key('company-id') : 
      custom_name_list.append(constants.INPUT_XML_CUST_CUSTOMER_INFO['company-id'])
   if constants.INPUT_XML_CUST_CUSTOMER_INFO.has_key('PriceGroup-id') : 
      custom_name_list.append(constants.INPUT_XML_CUST_CUSTOMER_INFO['PriceGroup-id'])
   ZONE_MODEL_NAME='_'.join(custom_name_list)

def create_ifw_rateadjust_inserts(date='2009-09-01'):
   if len(locals()) != 1:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_RATEADJUST (RATEPLAN,VERSION,RANK,VALID_FROM,VALID_TO,TIME_FROM,TIME_TO,QUANTITY_VALUE,USAGECLASS,USAGETYPE,SERVICECODE,SERVICECLASS,IMPACT_CATEGORY,SOURCE_NETWORK,DESTIN_NETWORK,DISCOUNT_TYPE,DISCOUNT_VALUE,NAME) values (ifw_seq_rateplan.currval,1,1,{date},null,'00:00',null,null,'.*','PBR','.*','.*','.*','.*','.*','N',0,'PBR Usage zero adjusment');\n"\
   .format(date=date)

   return sql_insert_query

def create_ifw_rateplan_cnf_inserts(service_code,ic_code):
   if len(locals()) != 2:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_RATEPLAN_CNF (RATEPLAN,VERSION,SERVICECODE,SERVICECLASS,IMPACT_CATEGORY,TIMEMODEL,TIMEZONE,MODEL_SELECTOR,PRICEMODEL,ALT_PRICEMODEL,PASSTHROUGH,ADDON_TYPE,ADDON_CHARGE) VALUES (ifw_seq_rateplan.currval,1,'service_code','DEF','{ic_code}',20001,20001,null,ifw_seq_pricemodel.currval,null,0,'P',0);\n"\
   .format(service_code=service_code,ic_code=ic_code)

   return sql_insert_query

def create_ifw_pricemdl_step_inserts(resourse_name,rum,beat,price,price_base,glid,min_charge='null',date='2009-09-01'):
   #min_charge is null when not passed
   #date will be 2009-09-01 if not passed
   if len(locals()) != 8:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_PRICEMDL_STEP (PRICEMODEL,VALID_FROM,RESOURCE_NAME,RUM,STEP,THRESHOLD_FROM,THRESHOLD_TO,BEAT,CHARGE,CHARGE_BASE,GLACCOUNT, MINIMUM_CHARGE) VALUES \
   (ifw_seq_pricemodel.currval,to_date( '{date} 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),'{resourse_name}','{rum}',1,0,999999999999999,{beat},{price},{price_base},'{glid}',{min_charge});\n"\
   .format(date=date,resourse_name=resourse_name,rum=rum,beat=beat,price=price,price_base=price_base,glid=glid,min_charge=min_charge)

   return sql_insert_query

def create_ifw_pricemodel_inserts(ic_code,name):
   if len(locals()) != 2:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_PRICEMODEL (PRICEMODEL,CODE,NAME,ROUNDING_METHOD,DECIMAL_PLACES) VALUES (ifw_seq_pricemodel.nextval,'{ic_code}','{name}','NONE',9);\n".format(ic_code=ic_code,name=name)

   return sql_insert_query
def create_ifw_rateplan_ver_inserts(date='2009-09-01'):
   if len(locals()) != 1:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_RATEPLAN_VER (RATEPLAN,VERSION,VALID_FROM,STATUS,ZONEMODEL,BASIC_RATEPLAN,BASIC_VERSION,BASIC) VALUES (ifw_seq_rateplan.currval,1,to_date( '{date} 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),'A',ifw_seq_zonemodel.currval,null,null,1);\n".format(date=date)

   return sql_insert_query

def create_ifw_rateplan_inserts(code,name,currency):
   if len(locals()) != 3:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_RATEPLAN (RATEPLAN,CODE,NAME,STATUS,SYSTEM_BRAND,MODELTYPE,SPLITTING,CALENDAR,UTC_TIME_OFFSET,CURRENCY,TAXTREATMENT) VALUES (ifw_seq_rateplan.nextval,'{code}','{name}','A',null,'R','1',20000,'+0000','{currency}',0);\n"\
   .format(code=code,name=name,currency=currency)

   return sql_insert_query
def create_ifw_impact_cat_inserts(code,name):
   if len(locals()) != 2:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_IMPACT_CAT (IMPACT_CATEGORY,RESULT,TYPE,NAME) VALUES ('{code}','{code}',0,'{name}');\n".format(code=code,name=name)

   return sql_insert_query

def create_ifw_apn_map_inserts(apn_group_id,rank,apn_expr,ic_code,ic_code_apn,date='2009-09-01'):
   if len(locals()) != 6:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_APN_MAP (APN_GROUP,RANK,SERVICECODE,ACCESSPOINTNAME,ZONE_WS,ZONE_RT,PDP_ADDRESS,NEW_ZONE_WS,NEW_ZONE_RT,ENTRYBY,ENTRYDATE,MODIFBY,MODIFDATE,MODIFIED,RECVER) VALUES ('{apn_group_id}',{rank},'GPR_O','{apn_expr}','{ic_code}','{ic_code}','.*','{ic_code_apn}','{ic_code_apn}',0,to_date( '{date} 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),207,to_date( '{date} 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),1,1);\n"\
   .format(apn_group_id=apn_group_id,rank=rank,apn_expr=apn_expr,ic_code=ic_code,ic_code_apn=ic_code_apn,date=date)

   return sql_insert_query
def create_ifw_apn_group_inserts(apn_group_id,apn_group_name,date='2009-09-01'):
   if len(locals()) != 3:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query = "INSERT INTO IFW_APN_GROUP (APN_GROUP,NAME,ENTRYBY,ENTRYDATE,MODIFBY,MODIFDATE,MODIFIED,RECVER) VALUES ('{apn_group_id}','{apn_group_name}',0,to_date( '{date} 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),null,to_date( '{date} 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),1,0);\n"\
   .format(apn_group_id=apn_group_id,apn_group_name=apn_group_name,date=date)

   return sql_insert_query

def create_ifw_zonemodel_inserts(g_rp_code,g_rp_name,apn_group_id='null'):
   if len(locals()) != 3:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   # print enterprise_info_dict
   sql_insert_query = "INSERT INTO IFW_ZONEMODEL (ZONEMODEL,CODE,NAME,MODELTYPE,FRAME,STATUS,APN_GROUP,GEOMODEL) VALUES (ifw_seq_zonemodel.nextval,'{g_rp_code}','{g_rp_name}','S','N','A','{apn_group_id}',null);\n"\
   .format(g_rp_code=g_rp_code,g_rp_name=g_rp_name,apn_group_id=apn_group_id)

   return sql_insert_query

def create_ifw_standard_zone_inserts(zone_descr,orig_zone_code,dest_zone_code,servicecode,ic_code,name,date='2009-09-01'):
   print(len(locals()))
   # $descr, $orig, $dest, $servicecode, $zone_ws, $name
# insert into ifw_standard_zone (zonemodel,description,origin_areacode,destin_areacode,servicecode,valid_from,valid_to,zone_ws,zone_rt,name,alt_zonemodel,recver) values 
# (ifw_seq_zonemodel.currval,'In Group A1','0001','00','GPR_O',to_date( '2009-09-01 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),null,'cxn0001001','cxn0001001','CXN_01900023_01900023SC01_SUB_PP01900023_GPRS_MO-In-Group-A1',null,0);
   if len(locals()) != 7:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)

   sql_insert_query = "INSERT INTO IFW_STANDARD_ZONE (ZONEMODEL,DESCRIPTION,ORIGIN_AREACODE,DESTIN_AREACODE,SERVICECODE,VALID_FROM,VALID_TO,ZONE_WS,ZONE_RT,NAME,ALT_ZONEMODEL,RECVER) VALUES \
   (ifw_seq_zonemodel.currval,'{zone_descr}','{orig_zone_code}','{dest_zone_code}','{servicecode}',to_date( '{date} 12:00:00 AM', 'YYYY-MM-DD HH:MI:SS AM'),null,'{ic_code}','{ic_code}','{name}',null,0);\n"\
   .format(zone_descr=zone_descr,orig_zone_code=orig_zone_code,dest_zone_code=dest_zone_code,servicecode=servicecode,date=date,ic_code=ic_code,name=name)

   return sql_insert_query
def create_cxn_zone_map_inserts(service_code, area, area_code, zone):
   if len(locals()) != 4:
      logger.error("Invalid number of arguments passed")
      sys.exit(1)
   sql_insert_query="INSERT INTO CXN_ZONE_MAP (ZONEMODEL, SERVICECODE, AREA, AREA_PREFIX, ZONE_CODE)\
   VALUES (ifw_seq_zonemodel.currval, '{service_code}', '{area}', '00{area_code}', '{zone}');\n".format(service_code=service_code,area=area,area_code=area_code,zone=zone)
   return sql_insert_query

def price_group_creation():
   utils.get_enterprise_info(constants.DCP_PRICING_PROCESSING_DIR+"/"+'shared_price_groups.xml')

def main():
   # pricing_constants.set_global_variable()
   logger.warning('Main function')
   pipeline_log_file_name='OPERATOR_NAME_OptionalEnterpriseName_OptionalPPID_{0}.sql'.format(constants.INSTANCE_TIME_STAMP)
   # mccmnc=utils.get_mccmnc(constants.DCP_PRICING_PROCESSING_DIR+"/"+'shared_price_groups.xml')
   # logger.debug("MCCMNC dictionary from input XML\n"+pprint.pformat(mccmnc))
   # price_group_creation(mccmnc)

   print "Constants set in main ",constants.INPUT_XML_CUST_CUSTOMER_INFO
   # print pprint.pformat(constants.INPUT_XML_MCCMNC)
   #sys.exit()
   #Create sample tests from price group XML
   #CXN_IFW_ID_SEQ
   # sql="SELECT TRIM(LAST_NUMBER) FROM USER_SEQUENCES WHERE SEQUENCE_NAME = 'CXN_IFW_ID_SEQ';"
   # sql="select to_char({op_abr}_IFW_ID_SEQ.nextval,'FM0000') from dual;".format(op_abr='CXN')
   # sqlplus_output = utils.run_sqlplus(constants.INF_ORA_LOGIN,constants.INF_ORA_PWD,constants.INF_ORA_DB,constants.DCP_IFW_SEQ_SQL.format(op_abr='CXN'))
   # if len(sqlplus_output) == 1:
      # enterprise_seq_id=sqlplus_output[0]
   # else:
      # logger.error("Error while fetching IFW SEQ")
   # print enterprise_seq_id
   # for line in sqlplus_output:
      # print(line)   
   # sqlCommand = 'select count(*) from account_t;'
   # queryResult, errorMessage = utils.runSqlQuery(sqlplus_script)
   # sqlplus_output = utils.run_sqlplus('dev10','dev10','BRM75DEV',sqlCommand)
   # for line in sqlplus_output:
      # print(line)       
   with open(pipeline_log_file_name, "a") as pipeline_sql_file:
      pipeline_sql_file.write("WHENEVER SQLERROR EXIT ROLLBACK\n")
      #CXN_01900023_01900023SC01_SUB_PP01900023_GPRS
      set_zone_model_name()
      print ZONE_MODEL_NAME
      # print constants.INPUT_XML_CUST_CUSTOMER_INFO['operator-abbr'].lower()+constants.INPUT_XML_CUST_ENTERPRISE_SEQ[constants.INPUT_XML_CUST_CUSTOMER_INFO['operator-id']]
      generated_ifw_zonemodel=create_ifw_zonemodel_inserts('cxn0001',ZONE_MODEL_NAME,'KKK')#variables#lists etc
      generated_ifw_standard_zone=create_ifw_standard_zone_inserts('In Group A1','0001','00','GPR_O','2009-09-01','cxn0001001','CXN_01900023_01900023SC01_SUB_PP01900023_GPRS_MO-In-Group-A1')#variables#lists etc
      for sql_insert_statement in generated_ifw_zonemodel+generated_ifw_standard_zone:
         pipeline_sql_file.write(sql_insert_statement)
      # for sql_insert_statement in generated_ifw_zonemodel:
         # pipeline_sql_file.write(sql_insert_statement)
      # for sql_insert_statement in generated_ifw_standard_zone:
         # pipeline_sql_file.write(sql_insert_statement)
      # for sql_insert_statement in create_cxn_zone_map_inserts('GPR_O','ORIG','0028967','0002'):
         # pipeline_sql_file.write(sql_insert_statement)
      # for sql_insert_statement in create_ifw_apn_group_inserts('cxn000101','CXN_01900023_01900023SC01_SUB_PP01900023_GPRS','2009-09-01'):
         # pipeline_sql_file.write(sql_insert_statement)       
      # for sql_insert_statement in create_ifw_apn_map_inserts('cxn000101',2,'apn1\.ericsson\.com','cxn0001001','cxn0001002','2009-09-01'):
         # pipeline_sql_file.write(sql_insert_statement)   
      # for sql_insert_statement in create_ifw_impact_cat_inserts('cxn0001001','CXN_01900023_01900023SC01_SUB_PP01900023_GPRS_MO-In_Group_A1'):
         # pipeline_sql_file.write(sql_insert_statement)   
      # for sql_insert_statement in create_ifw_rateplan_inserts('cxn0001001','CXN_01900023_01900023SC01_SUB_PP01900023_GPRS','EUR'):
         # pipeline_sql_file.write(sql_insert_statement)
      # for sql_insert_statement in create_ifw_pricemodel_inserts('cxn0001001','CXN_01900023_01900023SC01_SUB_PP01900023_GPRS_MO-In-Group-A1'):
         # pipeline_sql_file.write(sql_insert_statement)         
      # for sql_insert_statement in create_ifw_pricemdl_step_inserts('EURO','TTL',1000,1,1000000,'1930000','null','2009-09-01'):
         # pipeline_sql_file.write(sql_insert_statement)   
      # for sql_insert_statement in create_ifw_rateplan_cnf_inserts('TEL_O','cxn0001001'):
         # pipeline_sql_file.write(sql_insert_statement)        
      # for sql_insert_statement in create_ifw_rateadjust_inserts():
         # pipeline_sql_file.write(sql_insert_statement)  
      # date,resourse_name,rum,beat,price,price_base,glid,min_charge

      pipeline_sql_file.write("COMMIT;\nEXIT;\n")

