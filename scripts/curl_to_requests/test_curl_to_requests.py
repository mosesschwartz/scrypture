# test_curl_to_requests.py

import curl_to_requests
import subprocess

#curl_to_requests.curl_to_requests(input_text)

example_curl = '''curl http://www.google.com'''

scrypture_curl = '''curl 'https://scrypture.cirt.ibechtel.com/s/b64encode' -H 'Origin: https://scrypture.cirt.ibechtel.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'Authorization: Basic bXNjaHdhcjE6VGltTERBUHA0Mg==' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryfiIbAkkCVBNcc2eF' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36' -H 'Connection: keep-alive' -H 'Referer: https://scrypture.cirt.ibechtel.com/s/b64encode' --data-binary $'------WebKitFormBoundaryfiIbAkkCVBNcc2eF\r\nContent-Disposition: form-data; name="csrf_token"\r\n\r\n1428982056##ae85aea49ea61a10211059568649ea029eceff4f\r\n------WebKitFormBoundaryfiIbAkkCVBNcc2eF\r\nContent-Disposition: form-data; name="input_text"\r\n\r\nHello, this is a test!\r\n------WebKitFormBoundaryfiIbAkkCVBNcc2eF\r\nContent-Disposition: form-data; name="encode_or_decode"\r\n\r\nencode\r\n------WebKitFormBoundaryfiIbAkkCVBNcc2eF\r\nContent-Disposition: form-data; name="submit_button"\r\n\r\nConvert\r\n------WebKitFormBoundaryfiIbAkkCVBNcc2eF--\r\n' --compressed'''

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

