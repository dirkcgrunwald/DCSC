import boto
import boto.ec2
import os,sys,re,time

import utility

##
## A simple demo of the Boto EC2 interface.
##

EC2_ACCESS  = os.getenv('EC2_ACCESS_KEY')
EC2_SECRET  = os.getenv('EC2_SECRET_KEY')
S3_URL = utility.parse_url(os.getenv('S3_URL'))
EC2_URL = utility.parse_url(os.getenv('EC2_URL'))

if len(sys.argv) > 1:
    myKey = sys.argv[1]
else:
    myKey = ""

##
## For openstack @ futuregrid
##

region = boto.ec2.regioninfo.RegionInfo(
    name="nova", endpoint=EC2_URL[0])

connection = boto.connect_ec2(
    aws_access_key_id=EC2_ACCESS,
    aws_secret_access_key=EC2_SECRET,
    is_secure=False,
    region=region,
    port=EC2_URL[1],
    path=EC2_URL[2])

def find_my_instances(connection, key, verbose=False):
    mine = []
    reservations = connection.get_all_instances()
    for resv in reservations:
        for instance in resv.instances:
            if instance.key_name == key:
                if verbose:
                    print "Found key ", instance.key_name, "for instance", instance
                mine.append(instance)
    return mine

print "Here are all the instances..."
for resv in connection.get_all_instances():
    print "Reservation", resv
    for instance in resv.instances:
        print "....Instance ", instance.id, "with key", instance.key_name

if myKey != "":
    print "Now, here are all the instances for ", myKey
    mine = find_my_instances(connection, myKey)
    for instance in mine:
        print "....", instance, instance.state, instance.ip_address, instance.private_ip_address
