#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import pika
import traceback
import logging
logger = logging.getLogger()


class Processor:
    _name = ""
    _channel = None
    _callback = None

    def __init__(self, config, name, callback):
        self._name = name
        backpressure = "%2F?backpressure_detection=t"
        urlParameter = "amqp://%s/%s" % (config, backpressure)
        parameters = pika.URLParameters(urlParameter)
        connection = pika.BlockingConnection(parameters)
        self._channel = connection.channel()
        self._channel.queue_declare(queue=self._get_queue())
        self._callback = callback

    def _get_done_routing_key(self):
        return "done.processor.%s" % self._name

    def _get_queue(self):
        return "run.processor.%s" % self._name

    def run(self):
        self._channel.basic_consume(self.call_back_handler,
                                    queue=self._get_queue())
        self._channel.start_consuming()

    def call_back_handler(self, ch, method, properties, body):
        try:
            logger.info("%s callback start." % self._name)
            message = self._callback(body)
            if message is not None:
                self.push_task_done(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("%s callback end." % self._name)
        except Exception as err:
            logger.info("%s callback error,err:%s" % (self._name, err))
            traceback.print_exc()

    def push_task_done(self, message):
        self._channel.basic_publish(exchange='',
                                    routing_key=self._get_done_routing_key(),
                                    body=message)
