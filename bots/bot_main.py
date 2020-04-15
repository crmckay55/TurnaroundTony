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
        cs = CogSearchHelper()

        # TODO: seperate out document search bot.  send utterance to LUIS and call correct bot based on intent!
        lh.predict_rest(turn_context.activity.text)

        if not lh.haveintents:
            await turn_context.send_activity('I don\'t understand your question!')
        elif not lh.haveentities:
            await turn_context.send_activity('I wasn\'t able to extract your search terms.')
        else:
            for idx, entity in lh.entities.iterrows():
                if not cs.search(entity['text']):
                    await turn_context.send_activity(f"I can\'t find documents about {entity['text']}")
                else:
                    await turn_context.send_activity(f"I found these documents about {entity['text']}")
                    for idx, result in cs.results.iterrows():
                        await turn_context.send_activity(f"[{result['title']}]({result['url']}) - score: {result['@search.score']}")

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
