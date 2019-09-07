#This module is to create all the required configuration in pipeline database
#Class constants

import sys
import logging
from pricing_utils import *
logger = initialize_pricing_log(__name__)


def create_ifw_zonemodel_inserts():
    #print "hello"
	#buf = StringIO()
	# query = "insert into {0}({1},{2},{3}) values ({4}, {5}, {6})".format('users','name','age','dna','suzan',1010,'nda')
	# logger = logging.getLogger(__name__)	
	# logger = logging.getLogger(__name__ )
	# log = logging.getLogger('root')
	# logger = logging.getLogger(__main__)
	# logging.getLogger(__main__).warning('This is a pipeline warning')
	# logger = initialize_pricing_log(__name__)
	logger.warning('This is a pipeline 2 programme warning')
	sql_insert_query = "insert into ifw_zonemodel (zonemodel,code,name,modeltype,frame,status,apn_group,geomodel) values (ifw_seq_zonemodel.nextval,'$g_rp_code','$g_rp_name','S','N','A','$apn_group_id',null);\n"\
	.format('users','name','age','dna','suzan',1010,'nda')
	# query.format('users','name','age','dna','suzan',1010,'nda')
	#pipeline_sql_file.write(sql_insert_query)
	yield sql_insert_query
	# return (sql_insert_query)
    #print "insert into ifw_zonemodel (zonemodel,code,name,modeltype,frame,status,apn_group,geomodel) values (ifw_seq_zonemodel.nextval,'$g_rp_code','$g_rp_name','S','N','A','$apn_group_id',null);\n";

def main():

	# pricing_constants.set_global_variable()

	pipeline_log_file_name='OPERATOR_NAME_OptionalEnterpriseName_OptionalPPID.sql'
	#Create sample tests from price group XML
	with open(pipeline_log_file_name, "a") as pipeline_sql_file:
		pipeline_sql_file.write("WHENEVER SQLERROR EXIT ROLLBACK\n")
		generate_ifw_zonemodel=create_ifw_zonemodel_inserts()#variables#lists etc
		
		for sql_insert_statement in generate_ifw_zonemodel:
			pipeline_sql_file.write(sql_insert_statement)
		pipeline_sql_file.write("COMMIT;\nEXIT;\n")