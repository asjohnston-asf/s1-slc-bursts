# save all CMR umm_json metadata for S1 IW SLCs over the galapagos to disk
import json
import requests


def get_cmr_products(params):
    session = requests.Session()
    cmr_url = 'https://cmr.earthdata.nasa.gov/search/granules.umm_json'
    headers = {}
    products = []

    while True:
        response = session.get(cmr_url, params=params, headers=headers)
        response.raise_for_status()
        products.extend([item['umm'] for item in response.json()['items']])
        if 'CMR-Search-After' not in response.headers:
            break
        headers = {'CMR-Search-After': response.headers['CMR-Search-After']}

    return products


params = {
    'provider': 'ASF',
    'bounding_box': '-95,-4,-85,3',
    'short_name': [
        'SENTINEL-1A_SLC',
        'SENTINEL-1B_SLC',
    ],
    'attribute[]': 'string,BEAM_MODE,IW',
    'page_size': 2000,
}
granules = get_cmr_products(params)

with open('galapagos_slcs.json', 'w') as f:
    json.dump(granules, f)

