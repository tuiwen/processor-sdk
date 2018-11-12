#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from processor import Processor
import pika


class TestProcessor(unittest.TestCase):

    @patch("pika.BlockingConnection")
    @patch("pika.BlockingConnection.channel")
    def test_get_done_routing_key(self, mock_connection, mock_channel):
        mock_connection.return_value = None
        mock_connection.channel = None
        test_processor = Processor("", "test", None)
        key = test_processor._get_done_routing_key()
        self.assertEqual(key, "done.processor.test")

    @patch("pika.BlockingConnection")
    @patch("pika.BlockingConnection.channel")
    def test_get_queue(self, mock_connection, mock_channel):
        mock_connection.return_value = None
        mock_connection.channel = None
        test_processor = Processor("", "test", None)
        key = test_processor._get_queue()
        self.assertEqual(key, "run.processor.test")

    @patch("pika.BlockingConnection")
    @patch("pika.BlockingConnection.channel")
    def test_init_channel(self, mock_connection, mock_channel):
        backpressure = "%2F?backpressure_detection=t"
        urlParameter = "amqp://%s/%s" % (
            "guest:guest@127.0.0.1:5672", backpressure)
        parameters = pika.URLParameters(urlParameter)
        connection = pika.BlockingConnection(parameters)
        mock_connection.return_value = connection
        # mock_channel.return_value = connection.channel()
        test_processor = Processor("", "test", None)
        self.assertEqual(test_processor._channel, connection.channel())

    @patch("pika.BlockingConnection")
    @patch("pika.BlockingConnection.channel")
    def test_callback(self, mock_connection, mock_channel):
        backpressure = "%2F?backpressure_detection=t"
        urlParameter = "amqp://%s/%s" % (
            "guest:guest@127.0.0.1:5672", backpressure)
        parameters = pika.URLParameters(urlParameter)
        connection = pika.BlockingConnection(parameters)
        mock_connection.return_value = connection
        # mock_channel.return_value = connection.channel()
        test_processor = Processor("", "test", None)
        self.assertEqual(test_processor._callback, None)


if __name__ == '__main__':
    unittest.main()
