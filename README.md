Scrypture
============
Scrypture makes it easy to put Python scripts online. Simply add a class to your Python script and Scrypture will automatically serve your script through the web interface and API.

## Dev Environment Setup

Use GitHub client or git to clone to local directory
```Shell
cd $GITHUB/scrypture

# If you don't have pip installed, do this:
sudo easy_install pip
# On Debian-like distros you may instead use apt-get:
sudo apt-get install python-pip

# Install virtualenv
# This is not required, but is highly recommended
pip install virtualenv

# Create a virtualenv container in your directory
virtualenv venv

# Activate it. This basically overwrites your path so that when you run Python
# or other tools, it runs the local version inside venv instead of the system-
# wide version.
# type "deactivate" to exit the virtualenv
source venv/bin/activate

# Use pip to install all requirements
pip install -r requirements.txt

# If you run into errors, you may be missing some headers. Try:
# sudo apt-get install python-dev ncurses-dev

# Start script_utils with a local webserver
python scrypture.py
```
Point a web browser at http://localhost:5000, and you're done!

## Deploying

TODO
