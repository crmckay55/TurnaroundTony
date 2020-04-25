from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient, LUISRuntimeClientConfiguration
from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import requests
import json

import pandas as pd


class LuisHelper:

    def __init__(self):
        """
         Sends utterance to Luis and returns dataframes of intents and entities.

         :param self.top_intent: the highest ranked intent returned by LUIS
         :type  self.top_intent: str
         :param self.intents: all returned intents with intent and score
         :type  self.intents: pandas dataframe
         :param self.entities: all returned entities with role, type, text, and score
         :type  self.entities: pandas dataframe
         """

        __config = DefaultConfig()

        # TODO: do a check if configured and return a "not set up" message
        # TODO: Figure out how LUIS spell check works, or set up our own prior to sending to LUIS
        self.__runtime_key = __config.LUIS_API_KEY  # 'LUIS_RUNTIME_KEY'
        self.__runtime_endpoint = __config.LUIS_API_HOST_NAME  # 'LUIS_RUNTIME_ENDPOINT'
        self.__luisAppID = __config.LUIS_APP_ID  # 'LUIS_APP_ID'
        self.__luisSlotName = __config.LUIS_SLOT  # 'LUIS_APP_SLOT_NAME'
        # TODO: return error if not configured!!

        self.top_intent = ""
        self.intents = pd.DataFrame(columns=['intent', 'score'])
        self.entities = pd.DataFrame(columns=['role', 'type', 'text', 'score'])

    def predict_utterance(self, utterance) -> bool:
        """
        Sends utterance to LUIS and stores intents and entities that might be returned.

        :param utterance: the utterance to be analysed by LUIS
        :type utterance: str
        :return: Are there intents found in the utterance?
        :rtype: bool
        """

        # clear all values in case object is reused
        # TODO: figure out how to define variables properly in __init__ and here
        self.top_intent = ""
        self.intents.iloc[0:0]
        self.entities.iloc[0:0]

        headers = {}
        params = {
            'query': utterance,
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'true',           # TODO: learn what this parameter does!
            'staging': 'false',
            'subscription-key': self.__runtime_key
        }

        try:

            r = requests.get(
                f'{self.__runtime_endpoint}/luis/prediction/v3.0/apps/{self.__luisAppID}/slots/production/predict',
                headers=headers, params=params)

            data = json.loads(r.content)
            # content = json.dumps(data, indent=2)  # for debug print of content

        except Exception as e:  # call failed
            # TODO: no entities found error - figure out general error trapping and return to be captured
            print(f'{e}')
            return False

        # get all intents and scores
        try:
            for intent in data['prediction']['intents']:
                self.intents = self.intents.append({'intent': intent,
                                                    'score': data['prediction']['intents'][intent]['score']},
                                                   ignore_index=True)

            self.intents.sort_values(by=['score'], inplace=True, ascending=False)
            self.top_intent = data['prediction']['topIntent']
            print(self.intents)

        except Exception as e:  # no intents
            # TODO: no entities found error - figure out general error trapping and return to be captured
            pass  # no intents

        # get all entities and scores
        try:
            for role in data['prediction']['entities']['$instance']:
                for entity in data['prediction']['entities']['$instance'][role]:
                    self.entities = self.entities.append({'role': entity['role'],
                                                          'type': entity['type'],
                                                          'text': entity['text'],
                                                          'score': entity['score']},
                                                         ignore_index=True)

            self.entities.sort_values(by=['score'], inplace=True, ascending=False)
            print(self.entities)

        except Exception as e:  # no entities
            # TODO: no entities found error - figure out general error trapping and return to be captured
            pass  # no entities

        return True  # must be a good call b/c made it to here?


