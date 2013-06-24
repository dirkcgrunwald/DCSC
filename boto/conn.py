region = RegionInfo(name="eucalyptus", endpoint="149.165.146.135")

connection = boto.connect_ec2(
    aws_access_key_id="M0ZMS8AHLYCRZGCID4ZWO",
    aws_secret_access_key="m6JZgtWvZMpVhWFQ90FIzCISm9MFTocsPBfMmvX4",
    is_secure=False,
    region=region,
    port=8773,
    path="/services/Eucalyptus")

#Run commands

zones = connection.get_all_zones()

calling_format=boto.s3.connection.OrdinaryCallingFormat()
connection = boto.s3.Connection(aws_access_key_id="access key",
                      aws_secret_access_key="secret",
                      is_secure=False,
                      host="hostname",
                      port=8773,
                      calling_format=calling_format,
                      path="/services/Walrus")

#Run commands

bucket_instance = connection.get_bucket(bucket)
keys = bucket.get_all_keys()
for k in keys:
    #do something
