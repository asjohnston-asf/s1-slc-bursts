import os
import requests

import tqdm


headers = {
    'Content-Type': 'application/vnd.nasa.cmr.umm+json',
    'Echo-Token': os.environ['ECHO_TOKEN'],
}
collection_url = 'https://cmr.uat.earthdata.nasa.gov/ingest/providers/ASFDEV/collections/S1_SLC_BURSTS'
with open('cmr/S1_SLC_BURSTS.json') as f:
    collection_content = f.read()
response = requests.put(collection_url, data=collection_content, headers=headers)
print(response.content)


granule_url = 'https://cmr.uat.earthdata.nasa.gov/ingest/providers/ASFDEV/granules/'
directory = 'cmr/granules/'
headers = {
    'Content-Type': 'application/vnd.nasa.cmr.umm+json;version=1.6.4',
    'Echo-Token': os.environ['ECHO_TOKEN'],
}
session = requests.Session()
session.headers.update(headers)
for json_file in tqdm.tqdm(os.listdir(directory)):
    with open(directory + json_file) as f:
        content = f.read()
    granule_ur = json_file.split('.')[0]
    print(granule_ur)
    response = session.put(granule_url + granule_ur, data=content)
    print(response.text)
    response.raise_for_status()
