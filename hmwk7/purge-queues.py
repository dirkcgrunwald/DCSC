#!/usr/bin/env python
##
## Client that accepts messages encoded as integers
## computes the fibonacci of those numbers and returns
## a string representation
##

import pika

QHost = "sdr.cs.colorado.edu"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=QHost))

channel = connection.channel()

channel.queue_declare(queue='fib_to_compute', durable=True)
channel.queue_declare(queue='fib_from_compute', durable=True)

def purge_fib(ch, method, properties, body):
    print "Purge ", body
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(purge_fib, queue='fib_to_compute', no_ack=False)
channel.basic_consume(purge_fib, queue='fib_from_compute', no_ack=False)
channel.start_consuming()
