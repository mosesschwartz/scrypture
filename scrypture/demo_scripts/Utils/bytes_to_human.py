#!/usr/bin/env python
# .py
"""
Turns an integer value of nbytes into a human readable format
"""

from boltons import strutils
def bytes_to_human(bytes):
    '''Turns an integer value of nbytes into a human readable format'''
    try:
        b = int(bytes)
    except:
        b = 0
    return strutils.bytes2human(b)

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_list = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_list = form_input['input_list']
        if type(input_list) != list:
            input_list = input_list.split('\n')
        input_list = [t.strip() for t in input_list]

        output = '\n'.join(bytes_to_human(x for x in input_list))
        return {'output_type' : 'simple',
                'output' : output}
