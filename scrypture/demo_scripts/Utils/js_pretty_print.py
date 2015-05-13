#!/usr/bin/env python
# text_to_lower.py
"""
Runs jsbeautifier on inputted Javascript strings
"""

import jsbeautifier
def javascript_pretty_print(js):
    '''Runs jsbeautifier on inputted Javascript strings'''
    return jsbeautifier.beautify(js)


### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text'].encode('ascii','ignore')
        output = javascript_pretty_print(input_text)
        return {'output_type' : 'simple',
                'output' : output}
