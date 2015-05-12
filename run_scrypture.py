from scrypture import app
import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
print 'Starting Scrypture at http://localhost:5000'
app.run(threaded=True, host='0.0.0.0', debug=True)

