import logging
import json
# Create a custom logger
def initialize_pricing_log():
	
	logger = logging.getLogger(__name__)

	# Create handlers
	c_handler = logging.StreamHandler()
	f_handler = logging.FileHandler('dcp_pricing_test.log')
	c_handler.setLevel(logging.WARNING)
	f_handler.setLevel(logging.INFO)

	# Create formatters and add it to handlers
	c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
	f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	c_handler.setFormatter(c_format)
	f_handler.setFormatter(f_format)

	# Add handlers to the logger
	logger.addHandler(c_handler)
	logger.addHandler(f_handler)

	# logger.info('This is a warning')
	# logger.error('This is an error')


def read_config_file():
	with open('dcp_pricing_test.conf', 'r') as f:
		config = json.load(f)

	secret_key = config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
	ci_hook_url = config['CI']['HOOK_URL'] # 'web-hooking-url-from-ci-service'

	print secret_key