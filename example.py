
import filmography_matching
import json
import pathlib

with open(pathlib.Path.cwd() / 'example.json') as data:
    data = json.load(data)

for agent in data:
    
    result = filmography_matching.match_process(agent, 
        name_match_score=60, 
        title_match_score=100, 
        minimum_match_candidates=3)

    print(result)