#!/usr/bin/python
import boto
import boto.s3
import boto.s3.connection
import os,sys,re

import utility

def print_buckets(connection):
    rs = connection.get_all_buckets()
    for b in rs:
        print b.name

def print_keys(connection, bucket_instance):
    keys = bucket_instance.get_all_keys()
    for k in keys:
        print bucket_instance.name, "/", k.name

connection = utility.get_s3_connection_from_env()

if len(sys.argv) == 2:
    bucket_name = sys.argv[1]
    if utility.check_if_bucket_exists(connection, bucket_name):
        bucket_instance = connection.get_bucket(bucket_name)
        print_keys(connection, bucket_instance)
    else:
        print "Bucket", bucket_name, "doesn't exist"
else:
    print_buckets(connection)


