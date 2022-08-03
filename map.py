import json
import os
import xml.etree.ElementTree as ET

bursts = {}

dir = 'S1_burstid_20220530/IW/kml/'
for kml in os.listdir(dir):
    print(kml)
    tree = ET.parse(dir + kml)
    root = tree.getroot()
    for burst in root.iterfind('.//{http://www.opengis.net/kml/2.2}Placemark'):
        burst_id = burst.find('./{http://www.opengis.net/kml/2.2}name').text
        burst_id = burst_id.split(' ')[1] + '_' + burst_id.split(' ')[2]
        coordinate_string = burst.find('.//{http://www.opengis.net/kml/2.2}coordinates').text
        points = [
            {
                'Longitude': float(point.split(',')[0]),
                'Latitude': float(point.split(',')[1]),
            } for point in coordinate_string.split(' ')
        ]
        bursts[burst_id] = points

with open('burst_locations_by_id.json', 'w') as f:
    json.dump(bursts, f, separators=(',', ':'))
