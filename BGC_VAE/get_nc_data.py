import os
import pandas as pd
import requests

from pyesgf.search import SearchConnection
from tqdm import tqdm

def GetData(var, model='GFDL-ESM4', freq='Omon', exp='historical', grid='gr'):

    print("getting data")

    conn = SearchConnection('https://esgf-node.llnl.gov/esg-search', distrib=True)

    # experiment_id: data from 1850 - 2010
    # table_id: monthly oceanic and atmospheric data 

    for v in range(0, len(var)):

        print('getting results for variable ' + var[v])

        query = conn.new_context(
            latest=True,
            facets='null', 
            project='CMIP6',
            source_id = model,
            variable = var[v],
            table_id = freq,
            grid_label = grid,
            experiment_id = exp)

        # query = conn.new_context(
        #     latest=True,
        #     facets='null', 
        #     project='CMIP6',
        #     source_id ='GFDL-ESM4',
        #     variable = 'tos',
        #     table_id = 'Omon',
        #     grid_label = 'gr',
        #     experiment_id = 'historical')

        results = query.search()

        if len(results) == 0:
            print('no results for variable ' + var[v])
            continue

        # Weird exception the first time search() is called, we ignore it

        one_result = False

        try:
            results[0].file_context().search()

        except IndexError:
            one_result = True

        except Exception:
            print("shard exception raised: ignoring")
            pass

        if not one_result:
            print('warning: multiple files, selecting the first')
            hit = results[0].file_context().search()

        else: 
            hit = results.file_context().search()

        files = map(lambda f : {'filename': f.filename, 'url': f.download_url}, hit)
        files = list(files)
        files = pd.DataFrame.from_dict(files)

        for f in range(0, len(files)):        
            Download(files.url[f], files.filename[f])

    print("Done")

    # download

def Download(url, filename):

    if 'data' not in os.listdir():
        dir_path = os.path.join(os.getcwd(), 'data')
        os.makedirs(dir_path, exist_ok=True)

    elif filename in os.listdir('data'):
        print('file already exists: skipping')
        return

    os.chdir('data')

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
