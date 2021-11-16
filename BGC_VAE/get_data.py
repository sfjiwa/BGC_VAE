from pyesgf.search import SearchConnection
from tqdm import tqdm

def GetData():
    conn = SearchConnection('https://esgf-node.llnl.gov/esg-search', distrib=True)

    # experiment_id: data from 1850 - 2010
    # table_id: monthly oceanic and atmospheric data
    # variable: temperature, precipitation, mass_concentration_of_phytoplankton..., 

    query = conn.new_context(
        latest=True,
        facets='null', 
        project='CMIP6',
        source_id ='GFDL-ESM4',
        variable = 'tas,pr,chl',
        table_id = 'Omon, Amon',
        experiment_id = 'historical')

    results = query.search()

    # print("ID: ", results[0].json['id'])
    # print("Variables: ", results[0].json['variable'])

    hit_chl = results[0].file_context().search()
    hit_pr = results[1].file_context().search()
    hit_tas = results[2].file_context().search()

    files_chl = map(lambda f : {'filename': f.filename, 'url': f.download_url}, hit_chl)
    files_chl = list(files_chl)
    files_pr = map(lambda f : {'filename': f.filename, 'url': f.download_url}, hit_pr)
    files_pr = list(files_pr)
    files_tas = map(lambda f : {'filename': f.filename, 'url': f.download_url}, hit_pr)
    files_tas = list(files_tas)

    print("Done")