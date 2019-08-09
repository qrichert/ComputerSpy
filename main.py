#!/usr/bin/env python3

"""
Dependencies:
- pip install pyyaml
- pip install mss
- pip install pillow
"""

import os
import yaml
from logger import Logger


# Load configuration
settings = None
with open('config.yaml') as conf:
	try:
		settings = yaml.safe_load(conf)
	except yaml.YAMLError as exc:
		print(exc)

# Create log folder
if not os.path.isdir(settings['log_path']):
	os.mkdir(settings['log_path'])

# Create screenshot folder
if not os.path.isdir(os.path.join(settings['log_path'], 'screenshots/')):
	os.mkdir(os.path.join(settings['log_path'], 'screenshots/'))

if __name__ == '__main__':
	logger = Logger(settings)
	logger.logScreen()
