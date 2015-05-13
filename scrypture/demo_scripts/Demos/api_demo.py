#!/usr/bin/env python
# table_test.py
"""
Make a random table
"""

import argparse
import sys
import re
import json
import random
from scrypture import scrypture_api

### WebAPI ###
from scrypture import webapi
class WebAPI(webapi.WebAPI):
    submit_button = webapi.submit_button('Tabulate!')

    def run(self, form_input):
        s = scrypture_api.ScryptureAPI()
        silly1 = s.silly_demo()
        silly1_data = silly1['output']
        silly1_headers = silly1['headers']
        silly2 = s.silly_demo()
        silly2_data = silly2['output']
        silly2_headers = silly2['headers']

        return {'output_type' : 'table',
                'output' : silly2_data+silly1_data,
                'headers' : silly1_headers+silly2_headers}
