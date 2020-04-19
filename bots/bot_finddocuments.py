from botbuilder.core import ActivityHandler, TurnContext
from skills.luis_service import LuisHelper
from skills.cogsearch import CogSearchHelper


class BotFindDocs(ActivityHandler):

    @staticmethod
    async def find_docs(turn_context: TurnContext, lh: LuisHelper):
        cs = CogSearchHelper()

        if lh.has_entities:
            for search_term in lh.entities['text']:
                if not cs.search(search_term):
                    await turn_context.send_activity(f"I can\'t find documents about {search_term}")
                else:
                    await turn_context.send_activity(f"I found these documents about {search_term}")
                    for title, url, score in zip(cs.results['title'],
                                                 cs.results['url'],
                                                 cs.results['@search.score']):
                        await turn_context.send_activity(f"[{title}]({url}) - score: {score}")
        else:
            await turn_context.send_activity("I wasn\'t smart enough to find the search term in your question!")
