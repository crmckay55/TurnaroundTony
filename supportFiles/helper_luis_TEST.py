from helpers.helper_luis import LuisHelper
from config import DefaultConfig

cf = DefaultConfig

print("key", cf.LUIS_API_KEY)
print("slot", cf.LUIS_SLOT)
print("AppId", cf.LUIS_APP_ID)
print("Host", cf.LUIS_API_HOST_NAME)


luis = LuisHelper()

luis.predict({"query": "Do you have documents on task 1.1?"})
