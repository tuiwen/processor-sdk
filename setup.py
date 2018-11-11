#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for processor.

"""


from setuptools import setup

# Add here console scripts and other entry points in ini-style format
entry_points = """

# For example:
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    return body

test = Processor("127.0.0.1", "test", callback)
test.run()

"""


setup(
    name='processor.sdk',
    install_requires=[
        'bs4',
        'pika'
    ],
)
