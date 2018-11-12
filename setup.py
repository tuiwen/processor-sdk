#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for processor.

"""


from setuptools import setup, find_packages

# Add here console scripts and other entry points in ini-style format
entry_points = """

# For example:
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    return body

test = Processor("guest:guest@127.0.0.1:5672", "test", callback)
test.run()

"""


setup(
    name='processor.sdk',
    version="0.0.1",
    description="processor sdk",
    author="liguobao",
    package_dir={'': 'src'},
    install_requires=[
        'pika'
    ],
)
