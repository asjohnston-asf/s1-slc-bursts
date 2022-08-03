from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
import remotezip
import json

with open('galapagos_slcs.json') as f:
    granules = json.load(f)

auth = BotoAWSRequestsAuth(
    aws_host='s3-us-west-2.amazonaws.com',
    aws_region='us-west-2',
    aws_service='s3'
)
bucket = 'https://s3-us-west-2.amazonaws.com/asf-ngap2w-p-s1-slc-7b420b89/'

for granule in granules:
    url = bucket + granule['RelatedUrls'][0]['URL'].split('/')[-1]
    with remotezip.RemoteZip(url, auth=auth) as zip:
        filenames = [filename for filename in zip.namelist() if 'annotation/s1' in filename or filename.endswith('manifest.safe')]
        for filename in filenames:
            print(filename)
            zip.extract(filename, path='metadata/')
