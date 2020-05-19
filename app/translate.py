import json, uuid
import requests
from flask_babel import _
from flask import current_app




def translate(text, dest_language):
    with current_app.test_request_context():
        if 'MS_TRANSLATOR_KEY' not in current_app.config or \
                not current_app.config['MS_TRANSLATOR_KEY']:
            return _('Error: the translation service is not configured.')
        headers = {
            'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4()),
            'Ocp-Apim-Subscription-Region' : 'westeurope'
                }
        
        body = [{
            'text' : text
        }]

        r = requests.post('https://api.cognitive.microsofttranslator.com/'
                        '/translate?api-version=3.0&to={}'.format(dest_language),
                        headers=headers, json = body)
        if r.status_code != 200:
            return r.status_code
        res = json.loads(r.content.decode('utf-8-sig'))
        return res[0]['translations'][0]['text']




def detect(text):
    with current_app.test_request_context():
        if 'MS_TRANSLATOR_KEY' not in current_app.config or \
                not current_app.config['MS_TRANSLATOR_KEY']:
            return _('Error: the translation service is not configured.')
        headers = {
            'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4()),
            'Ocp-Apim-Subscription-Region' : 'westeurope'
                }
        
        body = [{
            'text' : text
        }]

        r = requests.post('https://api.cognitive.microsofttranslator.com/'
                        '/detect?api-version=3.0',
                        headers=headers, json = body)
        if r.status_code != 200:
            return r.status_code

        res = json.loads(r.content.decode('utf-8-sig'))
    
        return res[0]['language']