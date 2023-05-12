import pandas
import pathlib
import pydash
import requests
import tqdm

def value_extract(row, col):

    ''' Extract dictionary values. '''
  
    return pydash.get(row[col], "value")
   
def sparql_query(query, service):
 
    ''' Send sparql request, and formulate results into a dataframe. '''

    r = requests.get(service, params={"format": "json", "query": query})
    data = pydash.get(r.json(), "results.bindings")
    data = pandas.DataFrame.from_dict(data)
    for x in data.columns:
        data[x] = data.apply(value_extract, col=x, axis=1)
 
    return data

wikidata_path = pathlib.Path.cwd() / 'wikidata.parquet'

if not wikidata_path.exists():
    wikidata = pandas.DataFrame()
    for year in tqdm.tqdm(range(1880, 2025)):
        query = '''select ?film ?filmLabel ?title ?director ?directorLabel (year(?publication_date) as ?year) 
            where {
                ?film p:P31/wdt:P279* ?state .
                ?state ps:P31/wdt:P279* wd:Q11424 .
                ?film  wdt:P577 ?publication_date .
                filter (year(?publication_date) = '''+str(year)+''') .
                ?film wdt:P57 ?director
                optional { ?film wdt:P1476 ?title } .
                service wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}'''
        extract = sparql_query(query, "https://query.wikidata.org/sparql")
        wikidata = pandas.concat([wikidata, extract])

    for x in ['film', 'director']:
        wikidata[x] = wikidata[x].str.split('/').str[-1]

    wikidata = pandas.concat([
        wikidata[[x for x in wikidata.columns.values if x != 'filmLabel']],
        wikidata[[x for x in wikidata.columns.values if x != 'title']].rename(columns={'filmLabel':'title'})
        ]).dropna().drop_duplicates()

    wikidata = wikidata.rename(columns={
        'film':'film_id', 'director':'director_id', 'title':'film_label', 'directorLabel':'director_label'})
    
    wikidata = wikidata.astype(str)
    wikidata.to_parquet(wikidata_path)
else:
    wikidata = pandas.read_parquet(wikidata_path)

print(len(wikidata.film_id.unique()), 'film works.') 
