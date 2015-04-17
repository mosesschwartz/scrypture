'''Converts a cURL command to code for Python Requests'''

import argparse
import sys
import shlex
import urllib

def make_requests_code(url,
                       verb,
                       headers={},
                       params={},
                       data='',
                       savefile=None,
                       insecure=False,
                       username=None,
                       password=None,
                       auth=None):
    request_args = []
    code = 'import requests\n'
    if auth:
        if auth == 'basic':
            code += 'from requests.auth import HTTPBasicAuth\n'
            auth_func = 'HTTPBasicAuth(username,password)'
        elif auth == 'digest':
            code += 'from requests.auth import HTTPDigestAuth\n'
            auth_func = 'HTTPDigestAuth(username,password)'
        elif auth == 'ntlm':
            code += 'from requests_ntlm import HTTPNtlmAuth\n'
            auth_func = 'HTTPNtlmAuth(username,password)'
    if auth and not password:
        code += 'import getpass\n'
        code += 'password = getpass.getpass()\n'
    elif auth:
        code += 'username = \'' + username + '\'\n'
        code += 'password = \'' + password + '\'\n'
        request_args.append(auth_func)
    if headers != {}:
        code += 'headers = {}\n'.format(headers)
        request_args.append('headers=headers')
    if params != {}:
        code += 'params = \'\'\'{}\'\'\'\n'.format(repr(params))
        request_args.append('params=params')
    if data != '':
        code += 'data = \'\'\'{}\'\'\'\n'.format(data)
        request_args.append('data=data')
    if insecure == True:
        request_args.append('verify=False')

    code += 'r = requests.{}(\'{}\', {})\n'.format(verb,
                                                 url,
                                                 ', '.join(request_args))
    if savefile != None:
        save_fmt = 'with open(\'{}\',\'r\') as out:\n    out.write(r.text)\n'
        code += save_fmt.format(savefile)
    return code

def toggle(v):
    return not v

def ansi_c_quoting(s):
    '''shlex does not handle ANSI-C Quoting properly. Words of the form
    $'string' are treated specially. The word expands to string, with
    backslash-escaped characters replaced as specified by the ANSI C
    standard. This is a hacky workaround to parse these the way we want to.'''
    in_single_quotes = False
    in_double_quotes = False
    maybe_ansi_c_quote = False
    in_ansi_c_quote = False
    to_del = []
    s = list(s)

    for index, ch in enumerate(s):
        if ch == '\'':
            if in_ansi_c_quote:
                in_ansi_c_quote = toggle(in_ansi_c_quote)
                s[index] = '"'
            else:
                in_single_quotes = toggle(in_single_quotes)
        if ch == '"':
            if in_ansi_c_quote:
                s[index] = '\\"'
            else:
                in_double_quotes = toggle(in_double_quotes)
        if ch == '$' and not in_single_quotes and not in_double_quotes:
            maybe_ansi_c_quote = True
        if maybe_ansi_c_quote and ch == '\'':
            maybe_ansi_c_quote = False
            in_ansi_c_quote = True
            s[index] = '"'
            to_del.append(index-1)
        if in_ansi_c_quote and ch in '\a\b\f\n\r\t\v':
            s[index] = repr(ch)[1:-1]
    to_del.reverse()
    for i in to_del:
        del s[i]
    return ''.join(s)

def curl_to_requests(curl_str):
    parser = argparse.ArgumentParser(description='Do something awesome')
    parser.add_argument('target_url', type=str, nargs='?')
    parser.add_argument('-X', '--request', type=str, nargs=1, default='GET')
    parser.add_argument('-H', '--header', nargs=1, action='append', default=[])
    parser.add_argument('-d', '--data', nargs=1, action='append', default=[])
    parser.add_argument('--data-ascii', nargs=1, action='append', default=[])
    parser.add_argument('--data-binary', nargs=1, action='append', default=[])
    parser.add_argument('--data-urlencode', nargs=1, action='append', default=[])
    parser.add_argument('--digest', action='store_true')
    parser.add_argument('--ntlm', action='store_true')
    parser.add_argument('--anyauth', action='store_true') #BROKE!
    parser.add_argument('-e', '--referer', type=str)
    parser.add_argument('-F', '--form', nargs=1)
    parser.add_argument('-G', '--get', action='store_true', default=False)
    parser.add_argument('-I', '--head', action='store_true')
    parser.add_argument('-k', '--insecure', action='store_true')
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-O', '--remote_name', action='store_true')
    parser.add_argument('-r', '--range', type=str)
    parser.add_argument('-u', '--user', type=str)
    parser.add_argument('--url', type=str)
    parser.add_argument('-A', '--user-agent', type=str)
    parser.add_argument('--compressed', action='store_true', default=False)

    curl_str = curl_str.encode('ascii','ignore')
    curl_str = ansi_c_quoting(curl_str)
    curl_split = shlex.split(curl_str)
    try:
        args = parser.parse_known_args(curl_split[1:])[0]
    except:
        raise ValueError("Could not parse arguments. Is this a valid curl command?")

    url = args.target_url
    http_action = args.request.lower()
    header_dict = {h[0].split(':')[0]:h[0].split(':')[1]
                   for h in args.header}

    params_dict = {}#''.join(args.data_urlencode) #BROKEN
    for d in args.data_binary:
        print d
    data = ''.join([''.join(d)
            for d in args.data+args.data_ascii+args.data_binary])
    if data or args.form:
        # Send a POST request any time we have data
        http_action = 'post'
    if args.head:
        http_action = 'head'
    if args.get:
        # Unless we explicitly say to send a GET request, then send in URL
        http_action = 'get'
        params = urllib.urlencode(data)
    if args.user_agent:
        header_dict['User-Agent'] = args.user_agent
    if args.referer:
        header_dict['Referer'] = args.referer
    if args.range:
        header_dict['Range'] = args.range
    files = None
    if args.form:
        files = args.form

    savefile = None
    if args.remote_name:
        savefile = url.split('/')[-1]
    elif args.output:
        savefile = args.output

    username = None
    password = None
    if args.user:
        u = args.user
        if ':' in u:
            username,password = u.split(':')
        else:
            username = "'"+u+"'"
            password = 'getpass.getpass()'

    auth=None
    if args.digest:
        auth='digest'
    elif args.ntlm:
        auth='ntlm'
    elif username:
        auth='basic'

    if args.url:
        print "Unimplemented"
    if args.digest: #ntlm,
        print "Unimplemented"
    if args.form:
        print "Unimplemented"
    #also gotta implement the @file syntax
    # http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
    # And cookies!
    # And proxies!

    return make_requests_code(url,
                              http_action,
                              headers=header_dict,
                              params=params_dict,
                              data=data,
                              savefile=savefile,
                              insecure=args.insecure,
                              username=username,
                              password=password,
                              auth=auth)

if __name__ == '__main__':
    print curl_to_requests#(scrypture_curl)


