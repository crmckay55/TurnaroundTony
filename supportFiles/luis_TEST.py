from helpers.luis_service import LuisHelper

luis = LuisHelper()

luis.predict_utterance("Do you have any documents on task 1.1?")
