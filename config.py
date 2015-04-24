# config.py
import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'YOURSECRETKEY'
SCRIPTS_DIR = os.path.join(os.getcwd(), 'scripts')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files')
API_BASE_URL = 'https://localhost:5000/'
BOOTSTRAP_SERVE_LOCAL = True
SCRIPT_ROOT = '/'
LOCAL_DEV = True

