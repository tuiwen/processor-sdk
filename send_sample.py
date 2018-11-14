#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()


channel.queue_declare(queue='run.processor')

content = {"message": {"url": "https://www.biqugeg.com/17_17139/8388920.html"}}


channel.basic_publish(exchange='',
                      routing_key='run.processor.translation',
                      body=json.dumps(content))
print(" [x] Sent 'Hello World!'")
connection.close()
