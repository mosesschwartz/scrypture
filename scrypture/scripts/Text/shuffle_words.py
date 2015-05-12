#!/usr/bin/env python
# text_to_lower.py
"""
Randomly shuffle the words in a string (space delimeted)
"""

import random
def shuffle_words(s):
    '''Randomly shuffle the words in a string (space delimeted)'''
    s = s.split(' ')
    random.shuffle(s)
    s =' '.join(s)
    return s

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text']
        output = shuffle_words(input_text)
        return {'output_type' : 'simple',
                'output' : output}
