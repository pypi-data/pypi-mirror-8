# Flask-Celery-Helper

Even though the [Flask documentation](http://flask.pocoo.org/docs/patterns/celery/) says Celery extensions are
unnecessary now, I found that I still need an extension to properly use Celery in large Flask applications. Specifically
I need an init_app() method to initialize Celery after I instantiate it.

This extension also comes with a `single_instance` method using Redis locks.

[![Build Status](https://travis-ci.org/Robpol86/Flask-Celery-Helper.svg?branch=master)]
(https://travis-ci.org/Robpol86/Flask-Celery-Helper)
[![Coverage Status](https://img.shields.io/coveralls/Robpol86/Flask-Celery-Helper.svg)]
(https://coveralls.io/r/Robpol86/Flask-Celery-Helper)
[![Latest Version](https://pypip.in/version/Flask-Celery-Helper/badge.png)]
(https://pypi.python.org/pypi/Flask-Celery-Helper/)
[![Downloads](https://pypip.in/download/Flask-Celery-Helper/badge.png)]
(https://pypi.python.org/pypi/Flask-Celery-Helper/)
[![Download format](https://pypip.in/format/Flask-Celery-Helper/badge.png)]
(https://pypi.python.org/pypi/Flask-Celery-Helper/)
[![License](https://pypip.in/license/Flask-Celery-Helper/badge.png)]
(https://pypi.python.org/pypi/Flask-Celery-Helper/)

## Attribution

Single instance decorator inspired by
[Ryan Roemer](http://loose-bits.com/2010/10/distributed-task-locking-in-celery.html).

## Supported Platforms

* OSX and Linux.
* Python 2.6, 2.7, 3.3, 3.4
* [Flask](http://flask.pocoo.org/) 0.10.1
* [Redis](http://redis.io/) 2.9.1
* [Celery](http://www.celeryproject.org/) 3.1.11

## Quickstart

Install:
```bash
pip install Flask-Celery-Helper
```

Example:
```python
# example.py
from flask import Flask
from flask.ext.celery import Celery

app = Flask('example')
app.config['CELERY_BROKER_URL'] = 'redis://localhost'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'
celery = Celery(app)

@celery.task()
def add_together(a, b):
    return a + b

if __name__ == '__main__':
    result = add_together.delay(23, 42)
    print(result.get())
```

Run these two commands in separate terminals:
```bash
celery -A example.celery worker
python example.py
```

## Factory Example

```python
# extensions.py
from flask.ext.celery import Celery

celery = Celery()
```

```python
# application.py
from flask import Flask
from extensions import celery

def create_app():
    app = Flask(__name__)
    app.config['CELERY_IMPORTS'] = ('tasks.add_together', )
    app.config['CELERY_BROKER_URL'] = 'redis://localhost'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'
    celery.init_app(app)
    return app
```

```python
# tasks.py
from extensions import celery

@celery.task()
def add_together(a, b):
    return a + b
```

```python
# manage.py
from application import create_app

app = create_app()
app.run()
```

## Single Instance Example

```python
# example.py
import time
from flask import Flask
from flask.ext.celery import Celery, single_instance
from flask.ext.redis import Redis

app = Flask('example')
app.config['REDIS_URL'] = 'redis://localhost'
app.config['CELERY_BROKER_URL'] = 'redis://localhost'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'
celery = Celery(app)
Redis(app)

@celery.task(bind=True)
@single_instance
def sleep_one_second(a, b):
    time.sleep(1)
    return a + b

if __name__ == '__main__':
    task1 = sleep_one_second.delay(23, 42)
    time.sleep(0.1)
    task2 = sleep_one_second.delay(20, 40)
    results1 = task1.get(propagate=False)
    results2 = task2.get(propagate=False)
    print(results1)  # 65
    if isinstance(results2, Exception) and str(results2) == 'Failed to acquire lock.':
        print('Another instance is already running.')
    else:
        print(results2)  # Should not happen.
```

## Changelog

#### 1.0.0

* Support for non-Redis backends.

#### 0.2.2

* Added Python 2.6 and 3.x support.

#### 0.2.1

* Fixed single_instance arguments with functools.

#### 0.2.0

* Added include_args argument to single_instance.

#### 0.1.0

* Initial release.
