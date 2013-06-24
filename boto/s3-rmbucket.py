#!/usr/bin/python
import boto, boto.s3, boto.s3.key
import sys,os
import utility

if len(sys.argv) == 2:
    bucket_name = sys.argv[1]
else:
    print "Usage:", sys.argv[0],"<bucket>"
    sys.exit(1)

connection = utility.get_s3_connection_from_env()

if not utility.check_if_bucket_exists(connection, bucket_name):
    print "Bucket", bucket_name,"doesn't exist"
    sys.exit(3)
else:
    bucket_instance = connection.get_bucket(bucket_name)
    rs = bucket_instance.get_all_keys()
    for k in rs:
        print "Delete", k.name, "in", bucket_name
        bucket_instance.delete_key(k)
    print "Delete bucket", bucket_name
    bucket_instance.delete()
