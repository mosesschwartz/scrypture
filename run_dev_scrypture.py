from scrypture.scrypture import app, load_scripts, load_api, load_config
import logging
import sys

sys.path.append('/Users/moses/GitHub/scrypture_scripts')
import local_config
import sekrit

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
print 'Starting Scrypture at http://localhost:5000'
load_config('/Users/moses/GitHub/scrypture_scripts/local_config.py')
app.config['REGISTERED_SCRIPTS'] = local_config.REGISTERED_SCRIPTS
app.config['LOCAL_DEV'] = True
app.config['SCRYPTURE_USERNAME'] = sekrit.LDAP_USERNAME
app.config['SCRYPTURE_PASSWORD'] = sekrit.LDAP_PASSWORD
load_scripts()
load_api()
app.run(threaded=True, host='0.0.0.0', debug=True)
