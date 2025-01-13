#!/bin/bash

echo 'building and installing cryptoengine command line tool'

poetry build
pip install dist/cryptoengine-0.1.0.tar.gz

echo 'cryptoengine installed'
