import json

file = open('season.json','r')
season = json.load(file)
season_contents = season['content']
# print season_contents
season_urls = []
for content in season_contents:
    season_urls.append(content['urlFragment'])

print season_urls
