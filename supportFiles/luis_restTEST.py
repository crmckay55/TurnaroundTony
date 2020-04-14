########### Python 3.6 #############
import requests
from config import DefaultConfig

cf = DefaultConfig()

try:

    key = cf.LUIS_API_KEY
    endpoint = cf.LUIS_API_HOST_NAME
    appId = cf.LUIS_APP_ID
    utterance = 'do you have example org charts?'

    headers = {
    }

    params ={
        'query': utterance,
        'timezoneOffset': '0',
        'verbose': 'true',
        'show-all-intents': 'true',
        'spellCheck': 'false',
        'staging': 'false',
        'subscription-key': key
    }

    r = requests.get(f'https://{endpoint}/luis/prediction/v3.0/apps/{appId}/slots/production/predict',headers=headers, params=params)
    print(r.json())

except Exception as e:
    print(f'{e}')