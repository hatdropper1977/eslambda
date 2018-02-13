import json, jsonschema, string
from boto.connection import AWSAuthConnection
from chalice import Chalice
from chalicelib.config import DOCTYPE_NAME, ELASTIC_INDEX_NAME, ELASTICSEARCH_ENDPOINT
from datetime import datetime
from jsonschema import validate
from random import choice

schema = {
    "type" : "object",
    "properties" : {
        "anumber" : {"type" : "number"},
        "textblob" : {"type" : "string"},
        "agree" : {"type" : "boolean" },
        "ipaddr" : {
            "type" : "string",
            "format" : "ip-address"
        },     
    },
    "required" : ["anumber","textblob","ipaddr"],
    "additionalProperties" : False,
}

class ESConnection(AWSAuthConnection):

    def __init__(self, region, **kwargs):
        super(ESConnection, self).__init__(**kwargs)
        self._set_auth_region_name(region)
        self._set_auth_service_name('es')

    def _required_auth_capability(self):
        return [
         'hmac-v4']

def val_json(j):
    success = True
    try:
        validate(j,schema)
    except:
        success = False
    return success

def random_string_gen(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'):
    return ''.join(choice(chars) for _ in range(size))


client = ESConnection(region='us-east-1', host=ELASTICSEARCH_ENDPOINT, is_secure=False)
app = Chalice(app_name='helloworld')

@app.route('/', methods=['POST'],content_types=['application/json'])
def index():
    esdata = app.current_request.json_body
    if val_json(esdata):
        #ELASTICSEARCH_PATH = '/'.join((ELASTIC_INDEX_NAME, DOCTYPE_NAME.lower(), random_string_gen(), '_create?pretty'))
        t = datetime.now()
        esdata['@timestamp'] = t.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        ELASTICSEARCH_PATH = '/'.join((ELASTIC_INDEX_NAME, DOCTYPE_NAME.lower(),random_string_gen()))
        resp = client.make_request(method='POST', headers={'Content-Type': 'application/json'}, path='/' + ELASTICSEARCH_PATH, data=json.dumps(esdata))
        message = resp.read()
    else:
        message = 'Improper JSON'
    return message

@app.route('/info')
def index():
    resp = client.make_request(method='GET', path='/')
    return resp.read()
