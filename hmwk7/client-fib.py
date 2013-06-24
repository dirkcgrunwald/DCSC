#!/usr/bin/env python
##
## Client that accepts messages encoded as integers
## computes the fibonacci of those numbers and returns
## a string representation
##

import time
import fib_pb2

while True:
    try:
        import pika
        break
    except ImportError:
        print "Waiting for Pika to become available"
        time.sleep(1)

QHost = "sdr.cs.colorado.edu"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=QHost))

channel = connection.channel()

channel.queue_declare(queue='fib_to_compute', durable=True)
channel.queue_declare(queue='fib_from_compute', durable=True)

print ' [*] Waiting for messages. To exit press CTRL+C'

def fib(n):
    if n < 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def compute_fib(ch, method, properties, body):
    ##
    ## If we don't do an ACK, this message will not be consumed
    ## and will be re-delivered
    ##
    try:
        fiblist = fib_pb2.FibList()
        fiblist.ParseFromString(body)
        for fibInstance in fiblist.fibs:
            print "Compute fib(",fibInstance.n,")"
            fibInstance.response = str(fib(fibInstance.n))
        channel.basic_publish(exchange='',
                              routing_key='fib_from_compute',
                              body=fiblist.SerializeToString(),
                              properties=pika.BasicProperties(delivery_mode = 2))
    finally:
        ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(compute_fib, queue='fib_to_compute', no_ack=False)
channel.start_consuming()
