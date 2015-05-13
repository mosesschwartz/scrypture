#!/usr/bin/env python
# .py
"""
Converts a camelCased string to underscores
"""

from boltons import strutils
def camelcase_to_underscores(s):
    '''Converts a camelcased string to underscores'''
    return strutils.camel2under(s)


### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text']

        output = camelcase_to_underscores(input_text)
        return {'output_type' : 'simple',
                'output' : output}
