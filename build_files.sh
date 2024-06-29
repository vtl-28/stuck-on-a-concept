#!/bin/bash

# Navigate to the project directory
cd $(dirname $0)

pip install -r requirements.txt
python3.8 manage.py collectstatic