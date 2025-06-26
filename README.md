# Python STT Server

## Overview
This is a Python based RESTful API backend using the Django framework for converting speech to text with JWT authentication.

Speech to text engine used: https://github.com/ggml-org/whisper.cpp by https://github.com/ggml-org/whisper.cpp/commits?author=ggerganov

## Prerequisites:
- Python 3.11
- requests module -> pip install requests  
- docker 
- docker compose 

## Installation instructions
Cloning with submodules:
- git clone --recurse-submodules https://github.com/Oliver98t/Python_stt_server.git
- cd Python_stt_server
- docker compose up --builld -d

Update deatils for postgres database
- go to docker-compose.yml
- update the credentials under "db" and "environment" to your choosing

Create a superuser:
- in project root "Python_stt_server/" docker compose exec web python stt_server/manage.py        createsuperuser
- follow terminal suggestions
- record your username and password

## Testing
- replace username and password in test_api/test_api.py with your recorded credentials from creating the superuser
- in project root, cd test_api && python test_api.py

## Getting your Django secret for future reference
- in project root, docker compose exec web python stt_server/manage.py shell
- paste in to Python terminal 
    from django.core.management.utils import get_random_secret_key
    rint(get_random_secret_key())>>> print(get_random_secret_key())
- record your key and update stt_server/stt_server/settings.py "SECRET_KEY"
