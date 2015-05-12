import wtforms
import flask_wtf
import requests

class WebAPI(flask_wtf.Form):
    pass

def text_input(*args, **kwargs):
    '''
    Get multi-line text input as a strong from a textarea form element.
    '''
    text_input = wtforms.TextAreaField(*args, **kwargs)
    text_input.input_type = 'text'
    return text_input

def list_input(*args, **kwargs):
    '''
    Get a list parsed from newline-delimited entries from a textarea
    '''
    list_input = wtforms.TextAreaField(*args, **kwargs)
    list_input.input_type = 'list'
    return list_input

def line_input(*args, **kwargs):
    '''
    Get a single line of input as a string from a textfield
    '''
    line_input = wtforms.TextField(*args, **kwargs)
    line_input.input_type = 'line'
    return line_input

def password_input(*args, **kwargs):
    '''
    Get a password
    '''
    password_input = wtforms.PasswordField(*args, **kwargs)
    password_input.input_type = 'password'
    return password_input

def radio_field(*args, **kwargs):
    '''
    Get a password
    '''
    radio_field = wtforms.RadioField(*args, **kwargs)
    radio_field.input_type = 'radio_field'
    return radio_field

def submit_button(*args, **kwargs):
    '''
    Create a submit button
    '''
    submit_button = wtforms.SubmitField(*args, **kwargs)
    submit_button.input_type = 'submit_button'
    return submit_button

def multiple_input(*args, **kwargs):
    '''
    Multiline input
    '''
    multiline_input = wtforms.SelectMultipleField(*args, **kwargs)
    multiline_input.input_type = 'multiline'
    return multiline_input

def checkbox_field(*args, **kwargs):
    '''
    Checkbox field
    '''
    checkbox_field = wtforms.BooleanField(*args, **kwargs)
    checkbox_field.input_type = 'checkbox_field'
    return checkbox_field

def file_field(*args, **kwargs):
    '''
    File field
    '''
    file_field = wtforms.FileField(*args, **kwargs)
    file_field.input_type = 'file_field'
    return file_field

class PassHTTPAuthorizationHeader(requests.auth.AuthBase):
    '''
    Passes existing authorization header straight to the Request object.
    Useful if you already have access to an auth header but not username and
    password (e.g., user has authenticated to your server, and you want to
    reuse their authorization to access another server with the same user/pass)
    '''
    def __init__(self, header):
        self.header = header
    def __call__(self, r):
        r.headers['Authorization'] = self.header
        return r


