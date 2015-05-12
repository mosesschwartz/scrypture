#!/usr/bin/env python
# text_to_lower.py
"""
Reverse the words in a string
"""

def reverse_words(s):
    '''Reverse the words in a string (space delimeted)'''
    s =' '.join(reversed(s.split(' ')))
    return s

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text']
        output = reverse_words(input_text)
        return {'output_type' : 'simple',
                'output' : output}
