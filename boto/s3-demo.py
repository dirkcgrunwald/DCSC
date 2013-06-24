import boto
import boto.s3
import boto.s3.connection
import os,sys,re

import utility

##
## A simple demo of the Boto S3 interface.
## connect to futuregrid or OpenStack using the environment variables
## and then list the S3 buckets
##

EC2_ACCESS  = os.getenv('EC2_ACCESS_KEY')
EC2_SECRET  = os.getenv('EC2_SECRET_KEY')
S3_URL = utility.parse_url(os.getenv('S3_URL'))
EC2_URL = utility.parse_url(os.getenv('EC2_URL'))

calling_format=boto.s3.connection.OrdinaryCallingFormat()

connection = boto.s3.connection.S3Connection(
    aws_access_key_id=EC2_ACCESS,
    aws_secret_access_key=EC2_SECRET,
    is_secure=False,
    host=S3_URL[0],
    port=S3_URL[1],
    calling_format=calling_format,
    path=S3_URL[2])

print "Connection is ", connection

#Run commands

rs = connection.get_all_buckets()
for b in rs:
    print "bucket is ", b.name

print "Now, look for a specific bucket (dirk-bucket)"

bucket_instance = connection.get_bucket("dirk-bucket")
keys = bucket_instance.get_all_keys()
for k in keys:
    print "key is ", k

