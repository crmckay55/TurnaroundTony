from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient, LUISRuntimeClientConfiguration
from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import requests

import pandas as pd

import json


class LuisHelper:
    """Object to call LUIS and store intents and entities
    :param top_intent: the highest ranked intent returned by LUIS
    :type  top_intent: str
    :param intents: all returned intents with intent and score
    :type  intents: pandas dataframe
    :param self.entities: all returned entities with role, type, text, and score
    :type  entities: pandas dataframe
    :param haveintents: did LUIS find matching intent(s) for utterance?
    :type  haveintents: bool
    :param haveentities: did LUIS find entities in utterance?
    :type  haveentities: bool
    """

    def __init__(self):
        config = DefaultConfig()

        # TODO: do a check if configured and return a "not set up" message
        self._runtime_key = config.LUIS_API_KEY  # 'LUIS_RUNTIME_KEY'
        self._runtime_endpoint = config.LUIS_API_HOST_NAME  # 'LUIS_RUNTIME_ENDPOINT'
        self._luisAppID = config.LUIS_APP_ID  # 'LUIS_APP_ID'
        self._luisSlotName = config.LUIS_SLOT  # 'LUIS_APP_SLOT_NAME'
        self.top_intent = ""
        self.intents = pd.DataFrame(columns=['intent', 'score'])
        self.entities = pd.DataFrame(columns=['role', 'type', 'text', 'score'])
        self.haveintents = False
        self.haveentities = False

    def predict_rest(self, utterance):
        """Returns intents and entities for an utterance
        :param utterance: the utterance to be analysed by LUIS
        :type utterance: str
        """

        try:

            headers = {}
            params = {
                'query': utterance,
                'timezoneOffset': '0',
                'verbose': 'true',
                'show-all-intents': 'true',
                'spellCheck': 'false',
                'staging': 'false',
                'subscription-key': self._runtime_key
            }

            r = requests.get(
                f'{self._runtime_endpoint}/luis/prediction/v3.0/apps/{self._luisAppID}/slots/production/predict',
                headers=headers, params=params)

            result = r.json()
            print(result)

            # get all intents and scores
            if len(result['prediction']['intents']) > 0:
                self.top_intent = result['prediction']['topIntent']
                row = 0
                for intent in result['prediction']['intents']:
                    list = [intent, result['prediction']['intents'][intent]['score']]
                    self.intents.loc[row] = list
                    row += 1
                self.intents.sort_values(by=['score'], inplace=True, ascending=False)
                self.top_intent = result['prediction']['topIntent']
                self.haveintents = True
                print(self.top_intent)

            # get all entities and scores
            if len(result['prediction']['entities']['$instance']) > 0:
                row = 0
                for role in result['prediction']['entities']['$instance']:
                    for entity in result['prediction']['entities']['$instance'][role]:
                        list = [entity['role'], entity['type'], entity['text'], entity['score']]
                        self.entities.loc[row] = list
                        row += 1
                self.haveentities = True
                self.entities.sort_values(by=['score'], inplace=True, ascending=False)
                print(self.entities)

        except Exception as e:
            # TODO: return better error tracking
            print(f'{e}')
