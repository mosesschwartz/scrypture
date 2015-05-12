from scrypture import app
import logging
import sys

# Try loading a local_config.py file
#if os.path.isfile('local_config.py'):
#    app.config = AppConfig(app, 'local_config.py')
# If it isn't there, import config.py
# This is done to make it harder to lose local config changes when updating
#else:
#    app.config = AppConfig(app, 'scrypture.config.py')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
print 'Starting Scrypture at http://localhost:5000'
app.run(threaded=True, host='0.0.0.0', debug=True)

