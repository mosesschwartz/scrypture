#!/usr/bin/env python
# text_to_lower.py
"""
pretty print JSON
"""

import json
def json_pretty_print(s):
    '''pretty print JSON'''
    s = json.loads(s)
    return json.dumps(s,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))


### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text'].encode('ascii','ignore')
        output = json_pretty_print(input_text)
        return {'output_type' : 'simple',
                'output' : output}
