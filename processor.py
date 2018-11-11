#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import pika
import traceback
import logging
logger = logging.getLogger()


class Processor:
    name = ""
    channel = None
    callback = None

    def __init__(self, config, name, callback):
        self.name = name
        parameters = pika.URLParameters(config)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self._get_queue())
        self.callback = callback

    def _get_done_routing_key(self):
        return "done.processor.%s" % self.name

    def _get_queue(self):
        return "run.processor.%s" % self.name

    def run(self):
        self.channel.basic_consume(self.call_back_handler,
                                   queue=self._get_queue(),
                                   no_ack=True)
        self.channel.start_consuming()

    def call_back_handler(self, *args, **kwargs):
        try:
            logger.info("%s callback start." % self.name)
            message = self.callback(*args, **kwargs)
            self.push_task_done(message)
            logger.info("%s callback end." % self.name)
        except Exception as err:
            logger.info("%s callback error,err:" % (self.name, err))
            traceback.print_exc()

    def push_task_done(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self._get_done_routing_key(),
                                   body=message)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    return body


test = Processor("", "test", callback)
test.run()
