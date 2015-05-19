#!/usr/bin/env python
# module_template.py
"""
Convert simple, un-nested, JSON to CSV. Does not preserve any kind of
column order, but does deal with variable headers in different rows.

Example of acceptable input:
[
  {"field1" : "1", "field2" : "2"},
  {"field1" : "3", "fieldX" : "4"}
]

Output:
field2,fieldX,field1
2,,1
,4,3

"""

from __future__ import print_function
import argparse
import sys
import re
import csv
import json
import StringIO

def json_to_csv(json_input):
    '''
    Convert simple JSON to CSV
    Accepts a JSON string or JSON object
    '''
    try:
        json_input = json.loads(json_input)
    except:
        pass # If loads fails, it's probably already parsed
    headers = set()
    for json_row in json_input:
        headers.update(json_row.keys())

    csv_io = StringIO.StringIO()
    csv_out = csv.DictWriter(csv_io,headers)
    csv_out.writeheader()
    for json_row in json_input:
        csv_out.writerow(json_row)
    csv_io.seek(0)
    return csv_io.read()

### CLI ###

def main():
    """"This main function implements the CLI"""
    parser = argparse.ArgumentParser(description='Do something awesome')
    parser.add_argument('input_file', nargs=1,
                        type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', nargs='?',
                        type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    print(json_to_csv(args.input_file[0].read()), file=args.outfile)

if __name__ == '__main__':
    main()

### WebAPI ###

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    json_input = webapi.text_input('JSON')
    output_type = webapi.radio_field('Result',
                                     choices=[('string', 'Output as string'),
                                              ('file', "Download as file")],
                                     default='string')
    submit_button = webapi.submit_button('Convert')

    def run(self, form_input):
        json_input = form_input['json_input']
        output = json_to_csv(json_input)
        output_type = form_input['output_type']

        if output_type == 'string':
            return {'output_type' : 'simple',
                    'output' : output}
        elif output_type == 'file':
            return {'output_type' : 'file',
                    'filename' : 'json_to_csv.csv',
                    'output' : output}


