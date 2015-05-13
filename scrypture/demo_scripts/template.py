#!/usr/bin/env python
# .py
"""
{docstring}
"""

{script}

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Run')

    def run(self, form_input):
        input_text = form_input['input_text']
        timestamps = form_input['timestamps']
        if type(timestamps) != list:
            timestamps = timestamps.split('\n')
        timestamps = [t.strip() for t in timestamps]

        output = (input_text)

        return {'output_type' : 'simple',
                'output' : output}
