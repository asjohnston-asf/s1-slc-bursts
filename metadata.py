import json
import os

import remotezip


with open('galapagos_slcs.json') as f:
    granules = json.load(f)
    
headers = {'Cookie': f'asf-urs={os.environ["ASF_URS"]}'}

for granule in granules[:50]:
    url = granule['RelatedUrls'][0]['URL']
    url = url.replace('datapool', 'sentinel1')
    with remotezip.RemoteZip(url, headers=headers) as zip:
        filenames = [filename for filename in zip.namelist() if 'annotation/s1' in filename or filename.endswith('manifest.safe')]
        for filename in filenames:
            print(filename)
            zip.extract(filename, path='metadata/')
