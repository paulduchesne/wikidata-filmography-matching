from rapidfuzz import process, fuzz
import numpy
import pandas
import pathlib
import tqdm
import unidecode

def normalise_string(input_text):

    ''' Normalise text for matching purposes. '''

    normed = unidecode.unidecode(str(input_text).lower()).strip()

    return normed

def median_score(a_list, b_id, f, b_data):

    ''' Score the candidate based on median title match. '''

    test = b_data.loc[b_data.director_id.isin([b_id])]
    b_list = [normalise_string(x) for x in test.film_label.unique()]
    if len(a_list) < f or len(b_list) < 4:
        return 0

    my_score = [process.extractOne(normalise_string(a), b_list, scorer=fuzz.WRatio)[1] for a in a_list]
    return numpy.median(my_score)


def match_process(x, name_match_score=60, 
        title_match_score=100, 
        minimum_match_candidates=4):

    ''' Run process per source agent. '''
 
    wikidata_path = pathlib.Path.cwd() / 'wikidata.parquet'
    if not wikidata_path.exists():
        raise Exception('Wikidata export not available.')
    else:
        wikidata_data = pandas.read_parquet(wikidata_path)
    wikidata_data = wikidata_data.applymap(normalise_string)
            
    c = process.extract(normalise_string(x['agent_label']), wikidata_data.director_label.unique(), scorer=fuzz.WRatio, limit=200)
    c = [y[0] for y in c if y[1] > name_match_score]

    candidates = wikidata_data.loc[wikidata_data.director_label.isin(c)]

    result = dict()
    for y in candidates.director_id.unique():
        source_filmography = [normalise_string(z['film_label']) for z in x['filmography']]
        score = median_score(source_filmography, y, minimum_match_candidates, candidates)
        result[y] = score

    result = [k for k,v in result.items() if v >= title_match_score]

    if len(result) == 1:
        return {'source_id': x['agent_id'], 'wikidata_id': result[0].upper()}
