from botbuilder.core import ActivityHandler, TurnContext
from helpers.luis_service import LuisHelper
from helpers.cogsearch import CogSearchHelper


class BotFindDocs(ActivityHandler):

    @staticmethod
    async def search_staging_docs(turn_context: TurnContext, lh: LuisHelper):
        """
        Searches for documents and returns the titles with URL formatting, and the score.

        :param turn_context: passed turn context so bot can message from here
        :param lh: luis_helper object must be passed to access entities
        :return: none
        """
        cs = CogSearchHelper()

        if lh.has_entities:
            for search_term, search_role in zip(lh.entities['text'], lh.entities['role']):
                if not cs.search_staging_docs(search_term, search_role):
                    await turn_context.send_activity(f"I can\'t find documents about {search_term}")
                else:
                    await turn_context.send_activity(f"I found these documents about {search_role} {search_term}")
                    for title, url, score in zip(cs.results['title'],
                                                 cs.results['url'],
                                                 cs.results['@search.score']):
                        await turn_context.send_activity(f"[{title}]({url}) - score: {score}")
        else:
            await turn_context.send_activity("I wasn\'t smart enough to find the search term in your question!")
