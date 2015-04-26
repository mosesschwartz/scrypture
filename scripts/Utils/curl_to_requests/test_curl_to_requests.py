# test_curl_to_requests.py

import curl_to_requests
import subprocess

#curl_to_requests.curl_to_requests(input_text)

example_curl = '''curl http://www.google.com'''

tests = [example_curl]#, scrypture_curl]

for test in tests:
    req_code = curl_to_requests.curl_to_requests(test)
    exec(req_code)
    requests_out = r.text
    subprocess.call(test+' > tempfile',shell=True)
    curl_out = open('tempfile','r').read()
    if requests_out == curl_out:
        print 'Passed test'
    else:
        print 'Failed'
        print r.text

