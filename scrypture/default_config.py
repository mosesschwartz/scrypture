# config.py
import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'YOURSECRETKEY'
SCRIPTS_DIR = os.path.join(os.getcwd(), 'demo_scripts')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files')
API_BASE_URL = 'http://localhost:5000/'
BOOTSTRAP_SERVE_LOCAL = True
SCRIPT_ROOT = '/'
LOCAL_DEV = True
SCRYPTURE_USERNAME = "Nada"
SCRYPTURE_PASSWORD = "Nothing"

"""
To add another script, place the file inside the scripts package
and add the name to registered_scripts below. The loading code
will automagically find and import the script and put it into the
registered_modules dictionary.
"""
REGISTERED_SCRIPTS = ['Network.nmap_to_csv',
                      'Utils.json_to_csv',
                      'Utils.b64encode',
                      'Network.enumerate_ips',
                      'Security.quick_hash',
                      'Utils.convert_epoch_time',
                      'Security.file_hash',
                      'Demos.silly_demo',
                      'Demos.api_demo',
                      'Utils.curl_to_requests',
                      'Text.text_to_upper',
                      'Text.text_to_lower',
                      'Text.camelcase_to_underscores',
                      'Utils.js_pretty_print',
                      'Utils.json_pretty_print',
                      'Text.shuffle_words',
                      'Text.shuffle_characters',
                      'Text.reverse_words',
                      'Text.reverse_characters',
                      'Text.uniq',
                      'Testing.opendns_investigate',
                      'Testing.extract_iocs',
                      'Testing.universal_ioc_extractor',
                      'Testing.pdf_to_text',
                      'Testing.docx_to_text']
