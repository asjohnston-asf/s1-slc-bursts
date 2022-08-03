import json
import os
import xml.etree.ElementTree as ET

from shapely.geometry import Polygon


def get_attr_values(name, attributes):
    for attr in attributes:
        if attr['Name'] == name:
            return attr['Values']


with open('galapagos_slcs.json') as f:
    granules = json.load(f)
granules = [g for g in granules if g['TemporalExtent']['RangeDateTime']['BeginningDateTime'] >= '2021-11-11']

with open('burst_locations_by_id.json') as f:
    burst_map = json.load(f)

now = '2022-07-28T18:52:59.000Z'

for granule in granules:
    granule_ur = granule['DataGranule']['Identifiers'][0]['Identifier']
    directory = f'metadata/{granule_ur}.SAFE/annotation/'
    filenames = [directory + file for file in os.listdir(directory)]
    for filename in filenames:
        print(filename)
        tree = ET.parse(filename)
        root = tree.getroot()
        for burst in root.iterfind('.//burst'):
            sensing_time = burst.find('./sensingTime').text.split('.')[0]
            ascending_node_time = burst.find('./sensingTime').text
            relative_burst_id = burst.find('./burstId').text.rjust(6, '0')
            absolute_burst_id = burst.find('./burstId').attrib['absolute']
            swath = filename.split('-')[-8].upper()
            polarization = filename.split('-')[-6].upper()
            platform = filename.split('/')[-1][2]
            burst_ur = f'S1_SLC_{sensing_time.replace("-", "").replace(":", "")}_{polarization}_{relative_burst_id}_{swath}'
            points = burst_map[f'{relative_burst_id}_{swath}']
            polygon = Polygon([[point['Longitude'], point['Latitude']] for point in points])
            print(burst_ur)
            umm = {
                'TemporalExtent': {
                    'RangeDateTime': {
                        'BeginningDateTime': f'{sensing_time}Z',
                        'EndingDateTime': f'{sensing_time}Z',
                    },
                },
                'OrbitCalculatedSpatialDomains': granule['OrbitCalculatedSpatialDomains'],
                'GranuleUR': burst_ur,
                'AdditionalAttributes': [
                    {
                        'Name': 'GROUP_ID',
                        'Values': [
                            burst_ur,
                        ],
                    },
                    {
                        'Name': 'PROCESSING_TYPE',
                        'Values': [
                            'S1_SLC_BURSTS',
                        ],
                    },
                    {
                        'Name': 'POLARIZATION',
                        'Values': [
                            polarization,
                        ],
                    },
                    {
                        'Name': 'BEAM_MODE',
                        'Values': get_attr_values('BEAM_MODE', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'BEAM_MODE_TYPE',
                        'Values': get_attr_values('BEAM_MODE_TYPE', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'ASCENDING_DESCENDING',
                        'Values': get_attr_values('ASCENDING_DESCENDING', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'PATH_NUMBER',
                        'Values': get_attr_values('PATH_NUMBER', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'RELATIVE_BURST_ID',
                        'Values': [
                            str(int(relative_burst_id)),
                        ],
                    },
                    {
                        'Name': 'SWATH',
                        'Values': [
                            swath,
                        ],
                    },
                    {
                        'Name': 'SOURCE_SLC',
                        'Values': [
                            granule_ur,
                        ],
                    },
                    {
                        'Name': 'SV_POSITION_POST',
                        'Values': get_attr_values('SV_POSITION_POST', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'SV_POSITION_PRE',
                        'Values': get_attr_values('SV_POSITION_PRE', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'SV_VELOCITY_POST',
                        'Values': get_attr_values('SV_VELOCITY_POST', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'SV_VELOCITY_PRE',
                        'Values': get_attr_values('SV_VELOCITY_PRE', granule['AdditionalAttributes']),
                    },
                    {
                        'Name': 'ASC_NODE_TIME',
                        'Values': [
                            ascending_node_time,
                        ],
                    },
                    {
                        'Name': 'CENTER_LON',
                        'Values': [
                            str(polygon.centroid.x),
                        ],
                    },
                    {
                        'Name': 'CENTER_LAT',
                        'Values': [
                            str(polygon.centroid.y),
                        ],
                    },
                    {
                        'Name': 'LOOK_DIRECTION',
                        'Values': get_attr_values('LOOK_DIRECTION', granule['AdditionalAttributes']),
                    },
                ],
                'SpatialExtent': {
                    'HorizontalSpatialDomain': {
                        'Geometry': {
                            'GPolygons': [
                                {
                                    'Boundary': {
                                        'Points': burst_map[f'{relative_burst_id}_{swath}'],
                                    },
                                },
                            ],
                        },
                    },
                },
                'ProviderDates': [
                    {
                        'Date': now,
                        'Type': 'Insert',
                    },
                    {
                        'Date': now,
                        'Type': 'Update',
                    },
                ],
                'CollectionReference': {
                    'ShortName': 'S1_SLC_BURSTS',
                    'Version': '1',
                },
                'RelatedUrls': [
                    {
                        'URL': f'https://asj-dev.s3.us-west-2.amazonaws.com/bursts/data/{burst_ur}.tiff',
                        'Type': 'GET DATA',
                    }
                ],
                'DataGranule': {
                    'DayNightFlag': 'Unspecified',
                    'Identifiers': [
                        {
                            'Identifier': burst_ur,
                            'IdentifierType': 'ProducerGranuleId',
                        },
                    ],
                    'ProductionDateTime': now,
                    'ArchiveAndDistributionInformation': [
                        {
                            'Name': f'{burst_ur}.tiff',
                            'SizeInBytes': 1,
                        },
                    ],
                },
                'Platforms': [
                    {
                        'ShortName': 'Sentinel-1A' if platform == 'a' else 'Sentinel-1B',
                        'Instruments': [
                            {
                                'ShortName': 'C-SAR',
                            },
                        ],
                    },
                ],
                'MetadataSpecification': {
                    'URL': 'https://cdn.earthdata.nasa.gov/umm/granule/v1.6.4',
                    'Name': 'UMM-G',
                    'Version': '1.6.4',
                },
            }
            with open(f'cmr/granules/{burst_ur}.json', 'w') as f:
                json.dump(umm, f, indent=2)
