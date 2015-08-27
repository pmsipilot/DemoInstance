#!/usr/bin/python

import sys

sys.path.insert(1, "/opt/demoinstance/backend/")

from demoinstance.cli import cli_entrypoint
print "DemoInstance Dev Environment"
cli_entrypoint()

