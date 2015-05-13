#!/usr/bin/env python
# module_template.py
"""
eliminate duplicate lines, like `uniq`
"""

def uniq(lines):
    '''eliminate duplicate lines, like `uniq`'''
    lines = list(set(lines))
    return lines

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_lines = webapi.text_input('Lines')
    submit_button = webapi.submit_button('Convert')

    def run(self, form_input):
        input_lines = form_input['input_lines']
        if type(input_lines) != list:
            input_lines = [l.strip() for l in input_lines.split('\n')
                           if l != '']
        output = uniq(input_lines)
        return {'output_type' : 'simple',
                'output' : output}
