import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello to the Docker World! I have been seen {} times.\n'.format(count)

@app.route('/prime/<int:number>')
def show_prime_number(number):
    # show the user profile for that user
    return 'Number %d' % number




