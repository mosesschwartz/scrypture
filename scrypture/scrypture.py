"""
Scrypture makes it easy to put Python scripts online. Simply add a class to
your Python script and Scrypture will automatically serve your script through
the web interface and API.
"""

from flask import Flask, \
                  render_template, \
                  request, \
                  send_from_directory, \
                  Markup, \
                  jsonify, \
                  send_file, \
                  Response
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask.ext.restful import reqparse, abort, Api, Resource
from importlib import import_module
from collections import defaultdict, OrderedDict
import traceback
import inspect
import wtforms
import json
import logging
import os
import sys
import werkzeug.datastructures
from werkzeug import secure_filename
import hashlib
import tablib

app = Flask(__name__)
Bootstrap(app)
api = Api(app)

# Try loading a local_config.py file
#local_config_path = os.path.join(os.getcwd(), 'local_config.py')
#if os.path.exists(local_config_path):
#    AppConfig(app, local_config_path)
# If it isn't there, import config.py
# This is done to make it harder to lose local config changes when updating
#else:

def load_config(cfg_path):
    AppConfig(app, cfg_path)

def get_authorization():
    if app.config['LOCAL_DEV'] is True:
        import requests.auth
        username = app.config['SCRYPTURE_USERNAME']
        password = app.config['SCRYPTURE_PASSWORD']
        return requests.auth.HTTPBasicAuth(username, password)
    else:
        import webapi
        auth_header = request.environ.get('HTTP_AUTHORIZATION')
        auth = webapi.PassHTTPAuthorizationHeader(auth_header)
        return auth

@app.route('/', methods=['GET'])
def index():
    '''Return the main page'''
    return render_template('index.html',
                           scripts=registered_modules,
                           module_name='main')


@app.route('/script_index', methods=['GET'])
def script_listing():
    '''Return the index page listing all available modules'''
    return render_template('script_listing.html',
                           scripts=registered_modules)

@app.route('/about', methods=['GET'])
def about():
    '''About page'''
    return render_template('about.html',
                           scripts=registered_modules)

@app.route('/whoami', methods=['GET'])
def test():
    '''Shows diagnostic information'''
    return '<br>'.join(str(k)+' = '+str(v) for k,v in request.environ.items())

@app.route('/dl/<script_file_name>', methods=['GET'])
def download_script(script_file_name):
    '''Send a script directly from the scripts directory'''
    return "Sorry! Temporarily disabled."
    if script_file_name[:-3] in registered_modules:
        loaded_module = registered_modules[script_file_name[:-3]]
        package_path = os.sep.join(loaded_module.__package__.split('.')[1:])
        return send_from_directory(directory=os.path.join(
                                      app.config['SCRIPTS_DIR'],
                                      package_path),
                                   filename=script_file_name)
    else:
        return "ERROR"

@app.route('/dl/<file_id>/<path:file_name>')
def download_file(file_id, file_name):
    '''Download a file from UPLOAD_FOLDER'''
    extracted_out_dir = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    return send_file(os.path.join(extracted_out_dir, file_name))

@app.errorhandler(404)
def page_not_found(error):
    '''404 error handler'''
    return render_template('error.html',
                           scripts=registered_modules,
                           module_name=error,
                           error_message='Module not found'), 404

@app.errorhandler(500)
def server_error(error):
    '''500 error handler'''
    return render_template('error.html',
                           scripts=registered_modules,
                           module_name=error,
                           error_message='An error occurred! Sorry.'), 500

@app.route('/s/<module_name>', methods=['GET'])
def script_input(module_name):
    '''Render a module's input page. Forms are created based on objects in
    the module's WebAPI class.'''
    if module_name not in registered_modules:
        return page_not_found(module_name)
    form = registered_modules[module_name].WebAPI()
    return render_template('script_index.html',
                           form=form,
                           scripts=registered_modules,
                           module_name=module_name)

@app.route('/s/<module_name>', methods=['POST'])
def run_script(module_name):
    '''Take script input (from script_input above), run the run() function, and
    render the results in the appropriate template'''
    filename = ''
    #file_dir = ''
    #file_id = ''
    file_stream = ''
    if len(request.files) > 0:
        # Get the name of the uploaded file
        f = request.files['file_upload']

        # Make the filename safe, remove unsupported chars
        filename = secure_filename(f.filename)
        file_stream = f.stream
        #file_id = hashlib.md5(f.stream.read()).hexdigest()
        #f.stream.seek(0) # the save below won't work unless we  seek to 0

        #file_dir = os.path.join(app.config['UPLOAD_FOLDER'], file_id)

        #if not os.path.exists(file_dir):
        #    os.makedirs(file_dir)
        #f.save(os.path.join(file_dir,filename))
    try:
        form = werkzeug.datastructures.MultiDict(request.form)
        form['HTTP_AUTHORIZATION'] = get_authorization()
        form['filename'] = filename
        form['file_stream'] = file_stream
        #form['file_dir'] = file_dir
        #form['file_id'] = file_id
        result = registered_modules[module_name].WebAPI().run(form)
    except Exception:
        if app.config['LOCAL_DEV'] == True:
            raise # pass along to be caught by Flask's debugger
        return render_template('error.html',
                               scripts=registered_modules,
                               module_name=module_name,
                               error_message=traceback.format_exc())
    output = result['output']
    if 'output_type' in result:
        output_type = result['output_type']
    else:
        if isinstance(output, basestring):
            output_type = 'simple'
        else:
            output_type = 'table'
    if result['output_type'] == 'custom':
        return render_template('result_custom.html',
                               custom_output=Markup(result['output']),
                               scripts=registered_modules,
                               module_name=module_name)
    elif result['output_type'] == 'simple':
        return render_template('result.html',
                               output=result['output'],
                               scripts=registered_modules,
                               module_name=module_name)
    elif result['output_type'] == 'file':
        return Response(result['output'],
                        mimetype='application/octet-stream',
                        headers={'Content-Disposition':
                                 'attachment;filename='+result['filename']})
    elif result['output_type'] == 'table':
        return render_template('result_table.html',
                               output=result['output'],
                               scripts=registered_modules,
                               module_name=module_name,
                               headers=result['headers'])

def order_by_header(table, headers):
    '''Convert a list of dicts to a list or OrderedDicts ordered by headers'''
    ordered_table = []
    for row in table:
        # Tricky list comprehension got tricky when needing special handling
        # Lets do this the simplest way we can:
        row = {k:v for k,v in row.items() if k in headers}
        for h in headers:
            if h not in row:
                row[h] = ''
        ordered_row = OrderedDict(sorted(row.items(),
                                         key=lambda x:headers.index(x[0])))
        ordered_table.append(ordered_row)
    return ordered_table

def load_dataset(table, headers):
    data = tablib.Dataset()
    data.headers = headers
    data.dict = order_by_header(table, headers)
    return data

import datetime
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

@app.template_filter('to_json')
def to_json(table, headers):
    data = load_dataset(table, headers)
    data_json = json.dumps(data.dict,
                           default=json_serial,
                           indent=4, separators=(',', ': '))
    return data_json

@app.template_filter('to_html')
def to_html(table, headers):
    data = load_dataset(table, headers)
    html = data.html
    # Inject ID and styling
    html = html.replace('<table>',
        '<table id="output-table" class="table table-bordered">')
    return html

@app.template_filter('to_csv')
def to_csv(table, headers):
    data = load_dataset(table, headers)
    return data.csv

@app.template_filter('to_yaml')
def to_yaml(table, headers):
    data = load_dataset(table, headers)
    return data.yaml

@app.template_filter('to_repr')
def to_repr(table, headers):
    return repr(table)

@app.template_filter('to_trac')
def to_trac(table, headers):
    table = order_by_header(table, headers)
    header_row = ' || '.join(['{}'.format(h) for h in headers])
    wikiformatting = '|| {} ||\n'.format(header_row)
    for row in table:
        r = ' || '.join(['{}'.format(row[h]) for h in headers])
        wikiformatting += '|| {} ||\n'.format(r)
    wikiformatting = wikiformatting.replace('\r\n','')
    return wikiformatting

@app.template_filter('to_markdown')
def to_markdown(table, headers):
    table = order_by_header(table, headers)
    header_row = ' | '.join(['{}'.format(h) for h in headers])
    markdownformatting = '{}\n'.format(header_row)
    header_divider = '--- | ---'.join(['' for h in headers])
    markdownformatting += '{}\n'.format(header_divider)
    for row in table:
        r = ' | '.join(['{}'.format(row[h]) for h in headers])
        markdownformatting += '{}\n'.format(r)
    markdownformatting = markdownformatting.replace('\r\n','')
    return markdownformatting

@app.context_processor
def utility_processor():
    def make_navbar_links():
        nav_link_top = '''
        <li class="dropdown">

          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Scripts<span class="caret"></span></a>
          <ul class="dropdown-menu scrollable-menu" role="menu">'''
        nav_link_bottom = '''
          </ul>
        </li>'''
        packages = set([m.__package__ for k, m in registered_modules.items()])
        nav_links = ''
        for package in packages:
            nav_links += '''
            <li class="divider"></li>
            <li class="dropdown-header">{}</li>'''.format(package)
            for key,module in registered_modules.items():
                if module.__package__ == package:
                    nav_links += '''
            <li><a href="/s/{script}">{script}</a></li>'''.format(script=key)
        return Markup(nav_link_top+nav_links+nav_link_bottom)
    return dict(make_navbar_links=make_navbar_links)

registered_modules = {}

def load_scripts():
    # Add scrypture package package to the path before importing
    # so everything can import everything else regardless of package
    scrypture_dir = os.path.realpath(
                         os.path.abspath(
                           os.path.split(
                             inspect.getfile( inspect.currentframe() ))[0]))

    if scrypture_dir not in sys.path:
        sys.path.insert(0, scrypture_dir)

    # Load list of registered scripts
    registered_scripts = app.config['REGISTERED_SCRIPTS']

    for script in registered_scripts:
        try:
            s = import_module('.'+script,
                package=os.path.split(app.config['SCRIPTS_DIR'])[-1])
            s.package = s.__name__.split('.')[1]
            #remove package from script name:
            script_name = script.split('.')[-1]
            registered_modules[script_name] = s
        except Exception as e:
            logging.warning('Could not import ' + \
                            str(script)+': '+str(e.message))
            logging.debug(str(traceback.format_exc()))
            continue

def load_api():
    ### Set up the Scrypture API below ###

    # Field documentation at:
    # http://wtforms.simplecodes.com/docs/0.6/fields.html#basic-fields

    wtf_field_types = {'BooleanField' : str,
                       'DateField' : str,
                       'DateTimeField' : str,
                       'DecimalField' : str,
                       'FileField' : str,
                       'FloatField' : str,
                       'HiddenField' : str,
                       'IntegerField' : str,
                       'PasswordField' : str,
                       'RadioField' : str,
                       'SelectField' : str,
                       'SelectMultipleField' : str,
                       'TextAreaField' : str,
                       'TextField' : str}

    api_classes = {}

    parser = reqparse.RequestParser()
    for module_name, module in registered_modules.items():
        module_fields = []
        for attr_name, attr in inspect.getmembers(module.WebAPI):
            if type(attr) == wtforms.fields.core.UnboundField:
                for wtf_field_type in wtf_field_types:
                    if attr.field_class == getattr(wtforms, wtf_field_type):
                        module_fields.append((attr_name, wtf_field_type, attr.input_type))

        def api_class_factory():
            class ScriptAPI(Resource):
                module = None
                module_parser = None
                module_fields = None
                def get(self):
                    args = self.module_parser.parse_args()
                    kwargs = {}
                    for field_name, wtf_field_type, input_type in self.module_fields:
                        if wtf_field_type == 'TextAreaField':
                            if input_type == 'text':
                                kwargs[field_name] = json.loads(args[field_name])
                            else:
                                kwargs[field_name] = json.loads(args[field_name])
                        else:
                            kwargs[field_name] = json.loads(args[field_name])
                    kwargs['HTTP_AUTHORIZATION'] = get_authorization()
                    return self.module.WebAPI().run(kwargs)
            ScriptAPI.__name__ = 'scriptapi_{}'.format(module_name)
            return ScriptAPI

        api_class = api_class_factory()
        api_class.module = module
        api_class.module_parser = parser.copy()
        api_class.module_fields = module_fields

        for field_name, wtf_field_type, input_type in api_class.module_fields:
            api_class.module_parser.add_argument(field_name,
                                type=wtf_field_types[wtf_field_type],
                                required=True)
        api_classes[module_name] = api_class

    for module_name in registered_modules:
        api.add_resource(api_classes[module_name], '/api/v1/'+module_name)

    class ScriptDocumentation(Resource):
        def get(self):
            api_docs = {}
            for module_name, module in registered_modules.items():
                api_docs[module_name] = {
                    '__doc__' : module.__doc__,
                    'args' : [(arg.name, arg.type.__name__)
                              for arg in api_classes[module_name].module_parser.args]}
            return api_docs

    api.add_resource(ScriptDocumentation, '/api/v1/docs')









