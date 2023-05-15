from rapidfuzz import process, fuzz
import numpy
import pandas
import pathlib
import tqdm


def median_score(a_list, b_id, f, b_data):

    '''  '''

    test = b_data.loc[b_data.director_id.isin([b_id])]
    b_list = test.film_label.unique()
    if len(a_list) < f or len(b_list) < 4:
        return 0

    my_score = [process.extractOne(a,b_list, scorer=fuzz.WRatio)[1] for a in a_list]
    return numpy.median(my_score)


def match_process(x, name_match_score=60, 
        title_match_score=100, 
        minimum_match_candidates=4):

    '''  '''
 
    wikidata_path = pathlib.Path.cwd() / 'wikidata.parquet'
    if not wikidata_path.exists():
        raise Exception('Wikidata export not available.')
    else:
        wikidata_data = pandas.read_parquet(wikidata_path)

    c = process.extract(x['agent_label'], wikidata_data.director_label.unique(), scorer=fuzz.WRatio, limit=200)
    c = [y[0] for y in c if y[1] > name_match_score]

    candidates = wikidata_data.loc[wikidata_data.director_label.isin(c)]

    result = dict()
    for y in candidates.director_id.unique():
        source_filmography = [z['film_label'] for z in x['filmography']]
        score = median_score(source_filmography, y, minimum_match_candidates, candidates)
        result[y] = score

    result = [k for k,v in result.items() if v >= title_match_score]

    if len(result) == 1:
        return {'source_id': x['agent_id'], 'wikidata_id': result[0]}
