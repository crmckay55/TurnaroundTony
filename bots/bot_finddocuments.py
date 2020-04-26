from botbuilder.core import ActivityHandler, TurnContext
from helpers.luis_service import LuisHelper
from helpers.cogsearch import CogSearchHelper


class BotFindDocs(ActivityHandler):

    @staticmethod
    async def search_staging_docs(turn_context: TurnContext, lh: LuisHelper):
        """
        Searches for staging plan documents and returns the titles with URL formatting, and the score.
        The search is based on task number and/or search term/subject.

        :param turn_context: passed turn context so bot can message from here
        :type turn_context: TurnContext
        :param lh: luis_helper object must be passed to access entities
        :type lh: LuisHelper
        :return: none
        """
        cs = CogSearchHelper()

        if lh.entities.empty:
            await turn_context.send_activity("I wasn\'t smart enough to find the search term in your question!")

        else:
            for search_term, search_role in zip(lh.entities['text'],
                                                lh.entities['role']):

                if search_role == 'task':
                    filter_field = 'tasks'
                    filter_term = search_term
                    search_value = ''
                else:
                    filter_field = ''
                    filter_term = ''
                    search_value = search_term
                if not cs.search_staging_docs(filter_term, filter_field, search_value):
                    await turn_context.send_activity(f"I can\'t find documents about {search_role} {search_term}")

                else:
                    await turn_context.send_activity(f"I found these documents about {search_role} {search_term}")

                    for title, url, score in zip(cs.results['title'],
                                                 cs.results['url'],
                                                 cs.results['@search.score']):
                        await turn_context.send_activity(f"[{title}]({url}) - score: {score}")
                        # TODO: turn this into a JSON card
                        # TODO: consider adding a "send to me" button, or select docs and send?
