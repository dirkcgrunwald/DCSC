#!/usr/bin/python
import boto, boto.s3, boto.s3.key
import sys,os
import utility

if len(sys.argv) == 3 or len(sys.argv) == 4:
    bucket_name = sys.argv[1]
    key_name = sys.argv[2]
    if len(sys.argv) == 4:
        file_name = sys.argv[3]
    else:
        file_name = False
else:
    print "Usage:", sys.argv[0],"<bucket> <name> [<local-file>]"
    print "Stdin is used when no optional local-file is specified"
    sys.exit(1)

connection = utility.get_s3_connection_from_env()

if file_name != False and not os.path.isfile(file_name):
    print "File ", file_name, "doesn't exist"
    sys.exit(2)

if not utility.check_if_bucket_exists(connection, bucket_name):
    print "Creating bucket", bucket_name,"because it doesn't exist"
    connection.create_bucket(bucket_name)

bucket_instance = connection.get_bucket(bucket_name)
if utility.check_if_key_exists(bucket_instance, key_name):
    print "Key", key_name, "exists in bucket", bucket_name, "so contents will be overwritten"

k = boto.s3.key.Key(bucket_instance)
k.key = key_name
if file_name == False:
    k.set_contents_from_file(sys.stdin)
    print "Contents of bucket", bucket_name, ", key", key_name, "should be set stdin"
else:
    k.set_contents_from_file(open(file_name))
    print "Contents of bucket", bucket_name, ", key", key_name, "should be set from file ", file_name

