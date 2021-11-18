import os
import pandas as pd
import requests

from pyesgf.search import SearchConnection
from tqdm import tqdm

def GetData():

    print("getting data")

    conn = SearchConnection('https://esgf-node.llnl.gov/esg-search', distrib=True)

    # experiment_id: data from 1850 - 2010
    # table_id: monthly oceanic and atmospheric data
    # variable: temperature, precipitation, mass_concentration_of_phytoplankton..., 

    query = conn.new_context(
        latest=True,
        facets='null', 
        project='CMIP6',
        source_id ='GFDL-ESM4',
        variable = 'tos,chl',
        table_id = 'Omon',
        experiment_id = 'historical')

    results = query.search()

    # print("ID: ", results[0].json['id'])
    # print("Variables: ", results[0].json['variable'])

    # Weird exception the first time search() is called, we ignore it

    try:
        results[0].file_context().search()
    except Exception:
        print("shard exception raised: ignoring")
        pass


    hit_chl = results[0].file_context().search()
    hit_tos = results[2].file_context().search()

    files_chl = map(lambda f : {'filename': f.filename, 'url': f.download_url}, hit_chl)
    files_chl = list(files_chl)
    files_chl = pd.DataFrame.from_dict(files_chl)
    files_tos = map(lambda f : {'filename': f.filename, 'url': f.download_url}, hit_tos)
    files_tos = list(files_tos)
    files_tos = pd.DataFrame.from_dict(files_tos)

    Download(files_tos.url[0], files_tos.filename[0])
    Download(files_chl.url[0], files_chl.filename[0])

    # for index, row in files_chl.iterrows():
    #     if os.path.isfile(row.filename):
    #         print("File exists. Skipping.")
    #     else:
    #         Download(row.url, row.filename)

    # for index, row in files_pr.iterrows():
    #     if os.path.isfile(row.filename):
    #         print("File exists. Skipping.")
    #     else:
    #         Download(row.url, row.filename)

    # for index, row in files_tas.iterrows():
    #     if os.path.isfile(row.filename):
    #         print("File exists. Skipping.")
    #     else:
    #         Download(row.url, row.filename)

    print("Done")

    # download

def Download(url, filename):

    dir_path = os.path.join(os.getcwd(), 'data')
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)

    print("Downloading ", filename)
    r = requests.get(url, stream=True)
    total_size, block_size = int(r.headers.get('content-length', 0)), 1024
    with open(filename, 'wb') as f:
        for i in tqdm(r.iter_content(block_size),
                         total=total_size//block_size,
                         unit='KiB', unit_scale=True):
            f.write(i)
            
    if total_size != 0 and os.path.getsize(filename) != total_size:
        print("Downloaded size does not match expected size!\n",
              "FYI, the status code was ", r.status_code)

    os.chdir('../')
