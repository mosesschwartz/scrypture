#!/usr/bin/env python

from scrypture.scrypture import app, load_scripts, load_api, load_config
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
print 'Starting Scrypture at http://localhost:5000'
load_config('default_config.py')
load_scripts()
load_api()
app.run(threaded=True, host='0.0.0.0', debug=True)

