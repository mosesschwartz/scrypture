#!/usr/bin/env python
# module_template.py
"""
This is a simple utility to transform regular nmap output to CSV.
"""

from __future__ import print_function
import argparse
import sys
import re

def nmap_to_csv(nmap_output):
        entries = re.split('Nmap scan report for ', nmap_output)
        csv_out = 'ip,hostname,info\n'
        for entry in entries[1:]:
            entry_lines = entry.splitlines()
            ip_in_parens = re.findall('\(.*\)', entry_lines[0])
            if len(ip_in_parens) > 0:
                csv_out += ip_in_parens[0][1:-1]
                csv_out += ','
                csv_out += entry_lines[0]
            else:
                csv_out += entry_lines[0]
                csv_out +=','
            csv_out += ',"'
            csv_out += '\n'.join(entry_lines[1:])
            csv_out += '"\n'
        return csv_out

### CLI ###

def main():
    parser = argparse.ArgumentParser(description='Read NMAP output and convert to CSV')
    parser.add_argument('nmap_input', nargs=1, type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--outfile', nargs=1, type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()
    print(nmap_to_csv(args.nmap_input[0].read()), file=args.outfile)

if __name__ == '__main__':
    main()

### WebAPI ###
from scrypture import webapi
class WebAPI(webapi.WebAPI):
    nmap_output = webapi.text_input('NMAP Output')
    submit_button = webapi.submit_button('Convert to CSV')

    def run(self, form_input):
        nmap_output = form_input['nmap_output']

        output = nmap_to_csv(nmap_output)

        return {'output_type' : 'simple',
                'output' : output}

