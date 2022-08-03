# S1 SLC Burst DAAC Workflow

Creates a S1_SLC_BURSTS collection in CMR UAT for S1 IW SLCs covering the Galapagos Islands

1. `conda create -f environment.yml`
1. Run `cmr_search.py` to save all CMR umm_json metadata for  S1 IW SLCs over the Galapgos to disk
1. Download and extract https://sar-mpc.eu/files/S1_burstid_20220530.zip
   1. unzip the .kmz files to .kml format
   1. run `map.py` to create a json file mapping relative burst IDs (e.g. `045107_IW1`) to their bounding box
1. Run `metadata.py` or `metadata_s3.py` to extract the manifest.safe and annotation xml files for each SLC
   1. `metadata.py` requires an `asf-urs` cookie, `metadata_s3.py` requires AWS access keys
1. Run `cmr_granules.py` to generate umm_json metdata records for all granules since 2021-11-11 (when burst IDs started being included in SLC metadata)
1. Run `publish_to_cmr.py` to publish the collection record (`cmr/S1_SLC_BURSTS.json`) and all granule records to CMR
   1. requires an ECHO token, see https://wiki.earthdata.nasa.gov/display/ED/CMR+Data+Partner+User+Guide#CMRDataPartnerUserGuide-ToCreateaToken
