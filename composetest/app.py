import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

chosenNumber = 0

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

def set(value):
    retries = 5
    while True:
        try:
            return cache.set(chosenNumber,value)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get():
    retries = 5
    while True:
        try:
            return cache.get(chosenNumber)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello to the Docker World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<int:number>')
def show_prime_number(number):
	_number = number
	count = get_hit_count()
	_set = set(number)
	_get = get()
	if number > 1:
		for i in range(2,number):
			str = '{} is not a prime number <br/>'.format(_number)
			str2 = 'count: {}'.format(count)
			str3 = 'test: {}'.format(_get)
			
			
			return str + str3
		else:
			return '{} is a prime number'.format(_number)
	else:
		return '{} is not a prime number'.format(_number)





