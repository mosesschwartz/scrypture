#!/usr/bin/env python
# module_template.py
"""
Simple hash functions run on an uploaded file
"""

from __future__ import print_function
import os
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
    file_upload = webapi.file_field('File upload')
    hash_type = webapi.radio_field('What kind of hash?',
                                 choices=[('All', 'All'),
                                          ('MD5', 'MD5'),
                                          ('SHA1', 'SHA1'),
                                          ('SHA224', 'SHA224'),
                                          ('SHA256', 'SHA256'),
                                          ('SHA384', 'SHA384'),
                                          ('SHA512', 'SHA512')],
                                 default='All')
    submit_button = webapi.submit_button('Upload and Hash')

    def run(self, form_input):
        hash_type = form_input['hash_type']
        filename = form_input['filename']
        file_stream = form_input['file_stream']
        f = file_stream.read()
        output = hash(hash_type, f)

        return {'output_type' : 'table',
                'headers' : ['Algorithm','Hash'],
                'output' : output}
