This application get info about added photos, get photo locations and labels by Google Vision Api using Celery

## Requirements

Python3.6+, Django 1.11.6, bower, rabbitmq-server, celery

## Install rabbit sever for celery

```sudo apt-get install rabbitmq-server```

* Start worker for tests--

```celery -A instagram_alpha worker -l info```

## Install image packages

```sudo apt-get install libjpeg62 libjpeg62-dev zlib1g-dev libgraphicsmagick++-dev libboost-all-dev imagemagick python-dev libmagickwand-dev```
(http://sorl-thumbnail.readthedocs.io/en/latest/requirements.html)

## Install python packages
```pip install -r requirements.txt```

## Install bower components
cd dashboard/static
bower install

## Add google account key to env variables
export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_KEY_FILE

Add GOOGLE_MAPS_API_KEY, SECRET_KEY in settings




