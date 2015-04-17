API Documentation
============

Scrypture has an HTTP (~REST) API that is dynamically generated based on the members present in each module's WebAPI class, and a Python API that is is dynamically created based on the also-dynamically-created API reference at /api/v1/docs. The upside to this is that when scripts are added, the API is automatically updated. The downside is that it's impossible to debug.

All of the API functions take keyword arguments that are named the same as they are in the original Python module's WebAPI class.

All you need to do is download scrypture\_api.py and import it. The only dependency for your local machine is the requests library.

```
import scrypture_api
s = scrypture_api.ScryptureAPI()

# REST URI: http://localhost:5000/api/v1/b64encode?encode_or_decode="encode"&input_text="Hello, dear!"
test_string = "Hello, dear!"
b64encoded = s.b64encode(encode_or_decode='encode',
                         input_text=test_string)
print b64encoded

b64decoded = s.b64encode(encode_or_decode='decode',
                         input_text=b64encoded)
print b64decoded

# REST URI: http://localhost:5000/api/v1/json_to_csv?json_input=[{"field2": "2", "field1": "1"}, {"fieldX": "4", "field1": "3"}]
test_json = [{"field1" : "1", "field2" : "2"},
             {"field1" : "3", "fieldX" : "4"}]
csv = s.json_to_csv(json_input=test_json)
print csv
```
