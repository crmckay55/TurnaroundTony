#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978

    # the rest are set in the Azure app service plan as environmental variables:
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    LUIS_SLOT = 'staging'

    COG_SEARCH_KEY = os.environ.get("CogSearchKey", "")
    COG_SEARCH_HOST_NAME = os.environ.get("CogSearchHostName", "")
    COG_SEARCH_VERSION = '2019-05-06'
    COG_SEARCH_INDEX = 'indexes/metadata-index-v3/docs'

