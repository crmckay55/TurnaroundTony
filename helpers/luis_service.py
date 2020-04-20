from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient, LUISRuntimeClientConfiguration
from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import requests
import json

import pandas as pd


class LuisHelper:
    """
    Object to call LUIS and store intents and entities.

    :param self.top_intent: the highest ranked intent returned by LUIS
    :type  self.top_intent: str
    :param self.intents: all returned intents with intent and score
    :type  self.intents: pandas dataframe
    :param self.entities: all returned entities with role, type, text, and score
    :type  entities: pandas dataframe
    :param self.have_intents: did LUIS find matching intent(s) for utterance?
    :type  self.have_intents: bool
    :param self.have_entities: did LUIS find entities in utterance?
    :type  self.have_entities: bool
    """

    def __init__(self):
        config = DefaultConfig()

        # TODO: do a check if configured and return a "not set up" message
        # TODO: Figure out how LUIS spell check works, or set up our own prior to sending to LUIS
        self._runtime_key = config.LUIS_API_KEY  # 'LUIS_RUNTIME_KEY'
        self._runtime_endpoint = config.LUIS_API_HOST_NAME  # 'LUIS_RUNTIME_ENDPOINT'
        self._luisAppID = config.LUIS_APP_ID  # 'LUIS_APP_ID'
        self._luisSlotName = config.LUIS_SLOT  # 'LUIS_APP_SLOT_NAME'
        self.top_intent = ""
        self.intents = pd.DataFrame(columns=['intent', 'score'])
        self.entities = pd.DataFrame(columns=['role', 'type', 'text', 'score'])
        self.has_intents = False
        self.has_entities = False

    def predict(self, utterance):
        """Returns intents and entities for an utterance
        :param utterance: the utterance to be analysed by LUIS
        :type utterance: str
        :return has_intents: if intents are found returns TRUE
        """
        self.has_intents = False
        self.has_entities = False

        try:

            headers = {}
            params = {
                'query': utterance,
                'timezoneOffset': '0',
                'verbose': 'true',
                'show-all-intents': 'true',
                'spellCheck': 'true',
                'staging': 'false',
                'subscription-key': self._runtime_key
            }

            r = requests.get(
                f'{self._runtime_endpoint}/luis/prediction/v3.0/apps/{self._luisAppID}/slots/production/predict',
                headers=headers, params=params)

            data = json.loads(r.content)
            # content = json.dumps(data, indent=2)  # for debug print of content

            # get all intents and scores
            if data['prediction']['intents']:
                for intent in data['prediction']['intents']:
                    this_item = {'intent': intent, 'score': data['prediction']['intents'][intent]['score']}
                    self.intents = self.intents.append(this_item, ignore_index=True)

                self.intents.sort_values(by=['score'], inplace=True, ascending=False)
                self.top_intent = data['prediction']['topIntent']
                self.has_intents = True
                print(self.intents)

            # get all entities and scores
            if data['prediction']['entities']['$instance']:
                for role in data['prediction']['entities']['$instance']:
                    for entity in data['prediction']['entities']['$instance'][role]:
                        this_item = {'role': entity['role'], 'type': entity['type'], 'text': entity['text'],
                                     'score': entity['score']}
                        self.entities = self.entities.append(this_item, ignore_index=True)

                self.has_entities = True
                self.entities.sort_values(by=['score'], inplace=True, ascending=False)
                print(self.entities)

            return self.has_intents

        except Exception as e:
            # TODO: return better error tracking
            print(f'{e}')
            return self.has_intents
