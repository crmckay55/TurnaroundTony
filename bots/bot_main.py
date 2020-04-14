# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from helpers.luis import LuisHelper
from helpers.cogsearch import CogSearchHelper


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):

        await turn_context.send_activity(f"You said '{turn_context.activity.text}'")

        lh = LuisHelper()
        lh.predict(turn_context.activity.text)
        # await turn_context.send_activity(f"The top intent was: {lh.top_intent}")
        # await turn_context.send_activity(f"Your Sentiment was: {lh.sentiment}")
        # await turn_context.send_activity(f"And entities are: {lh.entities}")
        # TODO: Better error trapping, and handling of different bots and helpers

        cs = CogSearchHelper()

        cs.search(lh.entities)


        for idx, row in cs.results.iterrows():
            await turn_context.send_activity(f"Title : {row['title']}")
            await turn_context.send_activity(f"URL : {row['url']}")

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
