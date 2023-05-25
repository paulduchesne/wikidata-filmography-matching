Reusable function to identify agent matches with Wikidata.

#### Wikidata

An export of relevant Wikidata data is currently provided with the repository, although will obviously fall out of date immediately. Regenerating the export can be achieved with the `wikidata.py` script. The Wikidata export is configured to preference English titles, but this can be adjusted from within the SPARQL query.

#### Example

An source data example is provided as `example.json`

```json
[
    {
        "agent_id": "agent_001",
        "agent_label": "Jackie Weaver",
        "filmography": [
            {
                "film_id": "film_001",
                "film_label": "Picnic at Hanging Rock"
            },
            {
                "film_id": "film_002",
                "film_label": "The Removalists"
            },
            {
                "film_id": "film_003",
                "film_label": "Animal Kingdom"
            }
        ]
    }
]
```

This can be run via the `example.py` script, and will print matches to the terminal.

```
{'source_id': 'agent_001', 'wikidata_id': 'Q241897'}
```

Unsuccessful matches will currently not print anything.

#### Configuration

Available settings for the `filmography_matching` function are:
- name_match_score: This is the [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) score for the name match of the agent (100 being "exact match"). The default is 60, to allow for a reasonable pool of candidates and to incorporate possible name variations (eg F. W. Murnau, Friedrich Wilhelm Murnau).
- title_match_score: This is the [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) accepted mean score of all candidate "best title matches" per source titles. The match will only be accepted if there is exactly one remaining candidate.
- minimum_match_candidates: This imposes a minimum number of film credits on both sides. A higher number equates generally with a higher level of confidence, but will leave out matching individuals who have a lower number of credits in their filmography.

#### Known issues

- Successful matching depends on the source dataset being less well populated than Wikidata. This is due to the current method, which seeks to find best match for all titles present in the source agent filmography, and the general assumption that Wikidata will eventually outgrow other filmographic data sources.
- Agents with unusually large numbers of film credits (eg [Natalie Kalmus](https://en.wikipedia.org/wiki/Natalie_Kalmus)) are more likely to be falsely matches, owing to the larger pool of similar film titles. 
- Agents with similar names and filmographies present a disambiguation challenge, especially family members who frequently collaborated. There is a reasonable chance of confusion between organisations and individuals with similar names and filmographies, eg Walt Disney and Walt Disney Studios.
