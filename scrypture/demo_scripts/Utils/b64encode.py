#!/usr/bin/env python
# module_template.py
"""
Encode or decode base64 strings
"""

from __future__ import print_function
import base64
import re

def b64encode(s):
    return base64.encodestring(s)

def b64decode(s):
    return repr(str(base64.decodestring(s)))

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    encode_or_decode = webapi.radio_field('What do you want to do?',
                                 choices=[('encode', 'encode'),
                                          ('decode', "decode")],
                                 default='encode')
    submit_button = webapi.submit_button('Convert')

    def run(self, form_input):
        input_text = form_input['input_text']
        encode_or_decode = form_input['encode_or_decode']
        try:
            if encode_or_decode == 'encode':
                output = b64encode(input_text)
            elif encode_or_decode == 'decode':
                output = b64decode(input_text)
            else:
                output = "Stop messing with the form"
        except Exception, err:
            output = "ERROR: " + str(err)

        return {'output_type' : 'simple',
                'output' : output}
