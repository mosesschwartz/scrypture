#!/usr/bin/env python
# text_to_lower.py
"""
Reverse the characters in a string
"""

def reverse_characters(s):
    '''Reverse the characters in a string'''
    s =''.join(reversed(s))
    return s

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text']
        output = reverse_characters(input_text)
        return {'output_type' : 'simple',
                'output' : output}
