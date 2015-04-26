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
                  send_file
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask.ext.restful import reqparse, abort, Api, Resource
from importlib import import_module
from collections import defaultdict
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

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

app = Flask(__name__)
api = Api(app)
AppConfig(app, 'config.py')
Bootstrap(app)

"""
To add another script, place the file inside the scripts package
and add the name to registered_scripts below. The loading code
below will automagically find and import the script and put it into the
registered_modules dictionary.
"""
registered_scripts = ['Network.nmap_to_csv',
                      'Utils.json_to_csv',
                      'Utils.b64encode',
                      'Network.enumerate_ips',
                      'Security.quick_hash',
                      'Utils.convert_epoch_time',
                      'Security.file_hash',
                      'Demos.silly_demo',
                      'Utils.curl_to_requests',
                      'Text.text_to_upper',
                      'Text.text_to_lower',
                      'Text.camelcase_to_underscores',
                      'Text.js_pretty_print',
                      'Utils.json_pretty_print',
                      'Text.shuffle_words',
                      'Text.shuffle_characters',
                      'Text.reverse_words',
                      'Text.reverse_characters',
                      'Text.uniq']


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
        form['HTTP_AUTHORIZATION'] = request.environ.get('HTTP_AUTHORIZATION')
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
    elif result['output_type'] == 'table':
        return render_template('result_table.html',
                               output=json.dumps(result['output']),
                               scripts=registered_modules,
                               module_name=module_name,
                               headers=json.dumps(result['headers']))


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

@app.context_processor
def utility_processor():
    def make_navbar_links():
        nav_link_top = '''
        <li class="dropdown">

          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Scripts<span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu">'''
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

# Add scrypture package and scripts package to the path before importing
# so everything can import everything else regardless of package

cmd_folder = os.path.realpath(
               os.path.abspath(
                 os.path.split(
                   inspect.getfile( inspect.currentframe() ))[0]))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(
                  os.path.abspath(
                    os.path.join(
                      os.path.split(
                        inspect.getfile(
                          inspect.currentframe()))[0],"scripts")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

for script in registered_scripts:
    try:
        s = import_module('.'+script, package='scripts')
        s.package = s.__name__.split('.')[1]
        script_name = script.split('.')[-1] #remove package from script name
        registered_modules[script_name] = s
    except Exception as e:
        logging.warning('Could not import '+str(script)+': '+str(e.message))
        logging.debug(str(traceback.format_exc()))
        continue


### Set up the Scrypture API below ###
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
                kwargs['HTTP_AUTHORIZATION'] = request.environ.get('HTTP_AUTHORIZATION')
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

print 'Scrypture started at http://localhost:5000'

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', debug=True)
