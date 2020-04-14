from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import pandas as pd

import json


class LuisHelper:

    def __init__(self):
        config = DefaultConfig()

        # TODO: do a check if configured and return a "not set up" message
        self.runtime_key = config.LUIS_API_KEY  # 'LUIS_RUNTIME_KEY'
        self.runtime_endpoint = config.LUIS_API_HOST_NAME  # 'LUIS_RUNTIME_ENDPOINT'
        self.luisAppID = config.LUIS_APP_ID  # 'LUIS_APP_ID'
        self.luisSlotName = config.LUIS_SLOT  # 'LUIS_APP_SLOT_NAME'
        self.top_intent = ""
        self.intents = []
        self.sentiment = ""
        self.entities = []

        # Instantiate a LUIS runtime client
        self.clientRuntime = LUISRuntimeClient(self.runtime_endpoint, CognitiveServicesCredentials(self.runtime_key))

    def predict(self, utterance):
        # TODO: Better error trapping with messaging in the bot

        request = {"query": utterance}

        # Note be sure to specify, using the slot_name parameter, whether your application is in staging or production.
        response = self.clientRuntime.prediction.get_slot_prediction(app_id=self.luisAppID, slot_name=self.luisSlotName,
                                                                     prediction_request=request)


        if len(response.prediction.intents) > 0:
            self.intents = response.prediction.intents
            self.top_intent = response.prediction.top_intent
            self.sentiment = response.prediction.sentiment

        if len(response.prediction.entities) > 0:
            self.entities = response.prediction.entities['subject']


        print("Top intent: {}".format(response.prediction.top_intent))
        print("Sentiment: {}".format(response.prediction.sentiment))
        print("Intents: ")

        for intent in response.prediction.intents:
            print("\t{}".format(json.dumps(intent)))

        for entity in self.entities:
            print(f"Entity: {entity}")

