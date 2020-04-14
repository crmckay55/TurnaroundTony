from helpers.cogsearch import CogSearchHelper


csh = CogSearchHelper()


csh.search(['org chart'])


for idx, row in csh.results.iterrows():
    print(row['title'], row['url'])