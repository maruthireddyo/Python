import logging,pprint
import json
import subprocess
from subprocess import Popen, PIPE
import datetime
import xml.etree.cElementTree as ET
from pricing.utils.pricing_constants import *

# from contextlib import contextmanager
# Create a custom logger
# @contextmanager
# print(type(pricing_utils))

def initialize_pricing_log(module_name):
   # global logger
   # if logger is not None:
      # return
   logger = logging.getLogger(module_name)
   print datetime.datetime.now().strftime("%Y%m%d%H%M%S")
   # file_name='dcp_pricing_test_'+INSTANCE_TIME_STAMP+'.log'
   file_name='dcp_pricing_test.log'
   # Create handlers
   c_handler = logging.StreamHandler()
   f_handler = logging.FileHandler(file_name)
   c_handler.setLevel(logging.INFO)
   f_handler.setLevel(logging.ERROR)
   print "-------------------"

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
def get_mccmnc(input_file):

   print input_file
   mccmnc_dict={}
   inputxml = ET.parse(input_file).getroot()
   for zoneinfo in inputxml.findall('ZoneInfo'):
      if zoneinfo.attrib:
         print "Zone info attributes are ",zoneinfo.attrib
         for service_zone in zoneinfo.findall('OriginatingZone/*'):
            # print(service_zone)
            if service_zone.tag in ('DataZone','SMSZone','TelcoZone','SMSCZone'):
               mccmnc_dict.setdefault(service_zone.tag,{})
               # print "Data zone - ",service_zone.get('name')
               for mccmnc in service_zone.findall('MCCMNC'):
                  # print "MCCMNC - ",mccmnc.text
                  if service_zone.tag == 'TelcoZone':
                     mccmnc_dict[service_zone.tag].setdefault('MCCMNC',{})
                     mccmnc_dict[service_zone.tag]['MCCMNC'].setdefault(service_zone.get('name'),[])
                     mccmnc_dict[service_zone.tag]['MCCMNC'][service_zone.get('name')].append(mccmnc.text)
                  else:
                     mccmnc_dict[service_zone.tag].setdefault(service_zone.get('name'),[])
                     mccmnc_dict[service_zone.tag][service_zone.get('name')].append(mccmnc.text)
                  # mccmnc_dict.append(mccmnc.text)
         for service_zone in zoneinfo.findall('DestinationZone/*'):
            # print(service_zone)
            if service_zone.tag in ('TelcoZone'):
               mccmnc_dict.setdefault(service_zone.tag,{})
               # print "Data zone - ",service_zone.get('name')
               for callingcode in service_zone.findall('CallingCode'):
                  # print "MCCMNC - ",mccmnc.text
                  mccmnc_dict[service_zone.tag].setdefault('CallingCode',{})
                  mccmnc_dict[service_zone.tag]['CallingCode'].setdefault(service_zone.get('name'),[])
                  mccmnc_dict[service_zone.tag]['CallingCode'][service_zone.get('name')].append(callingcode.text)
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
   logger = initialize_pricing_log(__name__)
   logger.error('sqlplus_script')
   p = subprocess.Popen(['sqlplus','-S',connection],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   (stdout,stderr) = p.communicate(sqlplus_script.encode('utf-8'))
   stdout_lines = stdout.decode('utf-8').split("\n")
   print 'maruthi',stderr,'end'
   # print 'STDOUT:+++++++++++++++++++',stdout
   if stderr is not ' ':
      return stdout_lines
   # print 'STDERR:------------------------------------------------',stderr
   # return stdout_lines
# def get_global_value():
   # global global_variable
   # return global_variable

# def set_global_value(new_value):
   # global global_variable
   # global_variable = new_value
