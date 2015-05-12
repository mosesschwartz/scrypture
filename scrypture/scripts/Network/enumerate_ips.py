#!/usr/bin/env python
# module_template.py
"""
Print out every IP from a list of subnets in CIDR notation
"""

import argparse
import sys
import re
import netaddr

def get_ips_from_cidr_subnets(ip_subnets):
    ipnets = [netaddr.IPNetwork(ip) for ip in ip_subnets]
    return [str(ip) for ipnet in ipnets
                    for ip in ipnet]


### CLI ###
def main():
    """"This main function implements the CLI"""
    parser = argparse.ArgumentParser(description='Do something awesome')
    parser.add_argument('input_list', nargs='+',
                        type=str, default=sys.stdin)
    parser.add_argument('-o', '--outfile', nargs='?',
                        type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    input_list = args.input_list
    print '\n'.join(get_ips_from_cidr_subnets(input_list))

if __name__ == '__main__':
    main()

### WebAPI ###
from scrypture import webapi
class WebAPI(webapi.WebAPI):
    multi_input = webapi.list_input('Newline delimited indicators')
    submit_button = webapi.submit_button('Enumerate!')

    def run(self, form_input):
        multi_input = [x.rstrip() for x in re.split('\n', form_input['multi_input'])]

        output = '\n'.join(get_ips_from_cidr_subnets(multi_input))

        return {'output_type' : 'simple',
                'output' : output}

