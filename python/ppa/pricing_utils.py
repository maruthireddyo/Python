import logging
import json
# Create a custom logger
def initialize_pricing_log(module_name):
	
	logger = logging.getLogger(module_name)

	# Create handlers
	c_handler = logging.StreamHandler()
	f_handler = logging.FileHandler('dcp_pricing_test.log')
	c_handler.setLevel(logging.WARNING)
	f_handler.setLevel(logging.INFO)

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


def read_config_file(config_file_name):
	with open(config_file_name, 'r') as f:
		config = json.load(f)
		return(config)

# def get_global_value():
    # global global_variable
    # return global_variable

# def set_global_value(new_value):
    # global global_variable
    # global_variable = new_value		