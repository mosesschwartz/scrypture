#!/usr/bin/env python
# text_to_lower.py
"""
Randomly shuffle the characters in a string
"""

import random
def shuffle_characters(s):
    '''Randomly shuffle the characters in a string'''
    s = list(s)
    random.shuffle(s)
    s =''.join(s)
    return s

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text']
        output = shuffle_characters(input_text)
        return {'output_type' : 'simple',
                'output' : output}
