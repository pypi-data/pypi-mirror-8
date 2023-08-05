#!/bin/env python
# -*- coding: utf8 -*-

import argparse
import ConfigParser

from fedimg.consumers import KojiConsumer


# Read in config file
config = ConfigParser.RawConfigParser()
config.read('/etc/fedimg.cfg')

UTIL_USER = config.get('general', 'util_username')
TEST_USER = config.get('general', 'test_username')

# koji_server is the location of the Koji hub that should be used
# to initialize the Koji connection.
KOJI_SERVER = config.get('koji', 'server')

# The two slashes ("//") in the following URL are NOT a mistake.
BASE_KOJI_TASK_URL = config.get('koji', 'base_task_url')

# AMAZON WEB SERVICES (EC2)
AWS_ACCESS_ID = config.get('aws', 'access_id')
AWS_SECRET_KEY = config.get('aws', 'secret_key')
AWS_KEYNAME = config.get('aws', 'keyname')
AWS_KEYPATH = config.get('aws', 'keypath')
AWS_PUBKEYPATH = config.get('aws', 'pubkeypath')
AWS_TEST = config.get('aws', 'test')
AWS_AMIS = config.get('aws', 'amis')
AWS_IAM_PROFILE = config.get('aws', 'iam_profile')

# RACKSPACE
RACKSPACE_USER = config.get('rackspace', 'username')
RACKSPACE_API_KEY = config.get('rackspace', 'api_key')

# GCE
GCE_EMAIL = config.get('gce', 'email')
GCE_KEYPATH = config.get('gce', 'keypath')
GCE_PROJECT_ID = config.get('gce', 'project_id')

# HP
HP_USER = config.get('hp', 'username')
HP_PASSWORD = config.get('hp', 'password')
HP_TENANT = config.get('hp', 'tenant')
