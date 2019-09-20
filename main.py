#!/usr/bin/env python3

"""
Dependencies:
- pip install mss pillow pyyaml requests
- (or) pip install -r requirements.txt
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

if __name__ == '__main__':
	logger = Logger(settings)
	logger.logScreen()
