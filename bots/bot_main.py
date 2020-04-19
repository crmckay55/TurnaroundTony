# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from skills.luis_service import LuisHelper
from bots.bot_finddocuments import BotFindDocs


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):

        await turn_context.send_activity(f"You said '{turn_context.activity.text}'")

        lh = LuisHelper()

        if lh.predict(turn_context.activity.text):
            if lh.top_intent == 'search_stagingdocs':
                await BotFindDocs.search_staging_docs(turn_context, lh)
            else:
                await turn_context.send_activity('My overlords have not trained me yet to understand your message.')

        lh = None

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
