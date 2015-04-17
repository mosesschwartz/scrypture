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

words = json.load(open('dict.json','r'))

### WebAPI ###
import webapi
class WebAPI(webapi.WebAPI):
    submit_button = webapi.submit_button('Tabulate!')

    def run(self, form_input):
        headers = [random.choice(words) for x in xrange(5)]
        output = [{headers[x]:random.randint(0,100) for x in range(5)} for x in xrange(10)]

        return {'output_type' : 'table',
                'output' : output,
                'headers' : output[0].keys()}

