#!/usr/bin/env python
# text_to_upper.py
"""
Converts a string to all upper case
"""

def text_to_upper(s):
    '''Converts a string to all upper case'''
    return s.upper()

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text']
        output = text_to_upper(input_text)
        return {'output_type' : 'simple',
                'output' : output}
