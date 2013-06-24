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

print "EC2_URL is ", EC2_URL

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

print "Connection is ", connection

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

def wait_for_instance_to_be_public(instance, verbose=False):
    while True:
        if instance.state == 'running' and (instance.ip_address != instance.private_ip_address):
            return True
        else:
            if verbose:
                print "Waiting", (instance.state, instance.ip_address, instance.private_ip_address)
            time.sleep(3)
            instance.update()

def wait_for_reservation_to_be_public(reservation, verbose=False):
    for instance in reservation.instances:
        wait_for_instance_to_be_public(instance, verbose)
        

def kill_my_instances(connection, key, verbose=False):
    mine = find_my_instances(connection, key, verbose)
    ids = [instance.id for instance in mine]
    if len(ids) > 0:
        if verbose:
            print "Termiating instances", ids
        connection.terminate_instances(ids)

zones = connection.get_all_regions()
print "Available zones are ", zones

print "Here's my instances"
mine = find_my_instances(connection, "dcg-open")
for instance in mine:
    print "....", instance, instance.state, instance.ip_address, instance.private_ip_address
#    wait_for_instance_to_be_public(instance)

kill_my_instances(connection, "dcg-open", True)

print "Making new instance...."
newReservation = connection.run_instances(
    'ami-00000019',
    key_name = "dcg-open",
    instance_type = "m1.small")

print "Now waiting for that reservation group..."
wait_for_reservation_to_be_public(newReservation, True)
