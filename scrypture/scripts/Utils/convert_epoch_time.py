#!/usr/bin/env python
# module_template.py
"""
Convert epoch time (UNIX timestamps) to human readable form.
One per line.
"""

from __future__ import print_function
from datetime import datetime

def convert_epoch_time(t):
    try:
        return datetime.utcfromtimestamp(int(t)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Could not convert. Is this a valid timestamp?"

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    timestamps = webapi.text_input('Timestamp(s)')
    submit_button = webapi.submit_button('Convert')

    def run(self, form_input):
        timestamps = form_input['timestamps']
        if type(timestamps) != list:
            timestamps = timestamps.split('\n')
        timestamps = [t.strip() for t in timestamps]
        output = [{'Timestamp' : timestamp,
                   'Datetime' : convert_epoch_time(timestamp)}
                  for timestamp in timestamps
                  if timestamp != '']
        return {'output_type' : 'table',
                'headers' : ['Timestamp', 'Datetime'],
                'output' : output}
