from skills.cogsearch import CogSearchHelper


csh = CogSearchHelper()


csh.search_staging_docs(['org chart'])


for idx, row in csh.results.iterrows():
    print(row['title'], row['url'])