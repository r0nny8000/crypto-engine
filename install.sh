#!/bin/bash

echo 'building and installing cryp2bot command line tool'

poetry build
pip install dist/cryp2bot-0.1.0.tar.gz

echo 'cryp2bot installed'
 