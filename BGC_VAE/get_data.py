from pyesgf.search import SearchConnection
from tqdm import tqdm

def GetData():
    conn = SearchConnection('https://esgf-node.llnl.gov/esg-search', distrib=True)

    query = conn.new_context(
        latest=True,
        facets='null', 
        project='CMIP6',
        source_id ='GFDL-ESM4',
        experiment_id = 'ssp245',
        variable='o2',
        realm='ocnBgchem')

    results = query.search()
    print(results[0].json['id'])

    print("Done")