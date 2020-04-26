from config import DefaultConfig
import pandas as pd
import requests


class CogSearchHelper:

    def __init__(self):
        """
        Connects to cognitive services and stores results from search term.

        :param self.results: information found during search
        :type self.results: object
        """
        config = DefaultConfig

        self.__runtime_key = config.COG_SEARCH_KEY
        self.__runtime_endpoint = config.COG_SEARCH_HOST_NAME
        self.__runtime_version = config.COG_SEARCH_VERSION
        self.__runtime_index = f'indexes/{config.COG_SEARCH_INDEX}/docs'
        self.__headers = {'Content-Type': 'application/json',
                          'api-key': self.__runtime_key}
        self.results = pd.DataFrame()

    def search_staging_docs(self,
                            filter_term: str,
                            filter_field: str,
                            search_term: str) -> bool:
        """
        Uses cognitive search to find a search term, and then apply a filter.

        :param filter_field: what field should be filtered?  blank if none
        :type filter_field: str
        :param filter_term: what is the filter value for the filter field
        :type filter_term: str
        :param search_term: term to search for.  if blank, wildcard used
        :type search_term: str
        :return: Are there documents found?
        :rtype: bool
        """

        self.results = self.results.iloc[0:0]

        # TODO: return error if not configured

        print(f'Search: {filter_field}, {filter_term}, {search_term}')

        # base url
        url = self.__runtime_endpoint + self.__runtime_index + "?api-version=" + self.__runtime_version

        # if blank, wild card
        if search_term == '':
            url += "&search=*"
        else:
            url += "&search=" + search_term

        # add filter if present
        if filter_field != '':
            url += f"&%24filter={filter_field}%20eq%20'{filter_term}'"

        # TODO: wrap in try and raise error
        response = requests.get(url, headers=self.__headers)
        index_list = response.json()

        df = pd.json_normalize(index_list['value'])
        self.results = self.results.append(df, ignore_index=True)

        if not self.results.empty:
            return True
        else:
            return False
