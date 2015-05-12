'''Converts a cURL command to code for Python Requests'''
import curl2requests.curl_to_requests as curl_to_requests

from scrypture import webapi
class WebAPI(webapi.WebAPI):
    input_text = webapi.text_input('Input')
    submit_button = webapi.submit_button('Convert')

    def run(self, form_input):
        input_text = form_input['input_text'].strip()
        input_text = input_text.replace('\\\r\n','')
        input_text = input_text.replace('\\\r','')
        output = curl_to_requests.curl_to_requests(input_text)

        return {'output_type' : 'simple',
                'output' : output}
