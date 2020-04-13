from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig

import datetime, json, os, time


class LuisHelper:

    def __init__(self):
        config = DefaultConfig()

        self.runtime_key = config.LUIS_API_KEY  # 'LUIS_RUNTIME_KEY'
        self.runtime_endpoint = config.LUIS_API_HOST_NAME  # 'LUIS_RUNTIME_ENDPOINT'
        self.luisAppID = config.LUIS_APP_ID  # 'LUIS_APP_ID'
        self.luisSlotName = config.LUIS_SLOT  # 'LUIS_APP_SLOT_NAME'
        self.top_intent = ""
        self.sentiment = ""
        self.entities = ""


        # Instantiate a LUIS runtime client
        self.clientRuntime = LUISRuntimeClient(self.runtime_endpoint, CognitiveServicesCredentials(self.runtime_key))

    def predict(self, utterance):
        request = {"query": utterance}

        print(self.luisSlotName)

        # Note be sure to specify, using the slot_name parameter, whether your application is in staging or production.
        response = self.clientRuntime.prediction.get_slot_prediction(app_id=self.luisAppID, slot_name=self.luisSlotName,
                                                                     prediction_request=request)

        self.top_intent = response.prediction.top_intent
        self.sentiment = response.prediction.sentiment
        self.entities = response.prediction.entities

        print("Top intent: {}".format(response.prediction.top_intent))
        print("Sentiment: {}".format(response.prediction.sentiment))
        print("Intents: ")

        for intent in response.prediction.intents:
            print("\t{}".format(json.dumps(intent)))
        print("Entities: {}".format(response.prediction.entities))
