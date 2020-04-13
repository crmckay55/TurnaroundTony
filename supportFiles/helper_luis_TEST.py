from helpers.helper_luis import LuisHelper
from config import DefaultConfig


luis = LuisHelper()

luis.predict("Do you have any documents on task 1.1?")
