#!/usr/bin/env python
# module_template.py
"""
Simple hash functions
Warning! Does not strip any newlines or whitespace!
"""

from __future__ import print_function
import re
import hashlib

def hash(hash_type, input_text):
    '''Hash input_text with the algorithm choice'''
    hash_funcs = {'MD5' : hashlib.md5,
                  'SHA1' : hashlib.sha1,
                  'SHA224' : hashlib.sha224,
                  'SHA256' : hashlib.sha256,
                  'SHA384' : hashlib.sha384,
                  'SHA512' : hashlib.sha512}
    if hash_type == 'All':
        hash_type = ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512']
    else:
        hash_type = [hash_type]
    return [{'Algorithm' : h, 'Hash' : hash_funcs[h](input_text).hexdigest()}
            for h in hash_type]


### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    hash_type = webapi.radio_field('What kind of hash?',
                                 choices=[('All', 'All'),
                                          ('MD5', 'MD5'),
                                          ('SHA1', 'SHA1'),
                                          ('SHA224', 'SHA224'),
                                          ('SHA256', 'SHA256'),
                                          ('SHA384', 'SHA384'),
                                          ('SHA512', 'SHA512')],
                                 default='All')
    submit_button = webapi.submit_button('Hash')

    def run(self, form_input):
        input_text = form_input['input_text']
        hash_type = form_input['hash_type']

        output = hash(hash_type, input_text)

        return {'output_type' : 'table',
                'headers' : ['Algorithm','Hash'],
                'output' : output}
