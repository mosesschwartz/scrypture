script_utils
============
script\_utils is a web application wrapper around Python scripts, implemented by adding a WebAPI class to almost any existing Python module. Every script_utils module can be downloaded directly from this site and may be run on the command line or imported as a module.

This is version 2.0, and it's slightly less barebones than version 1.0. New additions are:
 * HTTP (REST) API
 * Python API
 * Scripts can be created with the API and hosted on script_utils, allowing the creation of more complex workflows

To install:

Use GitHub client or git to clone to local directory
```Shell
cd $GITHUB/script_utils

# If you don't have virtualenv installed, do this:
sudo easy_install pip
pip install virtualenv

# Create a virtualenv container in your directory
virtualenv venv

# Activate it. This basically overwrites your path so that when you run Python or other
# tools, it runs the local version inside venv instead of the system-wide version
# type "deactivate" to exit the virtualenv
source venv/bin/activate

# Use pip to install all requirements
pip install -r requirements.txt

# Start script_utils with a local webserver
python script_utils.py
```
Point a web browser at localhost:5000, and you're done!
