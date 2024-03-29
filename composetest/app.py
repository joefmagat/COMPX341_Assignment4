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

def lpush(value): #stored the inputed number into a list in redis
    retries = 5
    while True:
        try:
            return cache.lpush('primeList',value)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def lrange(): #gets the whole list from redis
    retries = 5
    while True:
        try:
         #return cache.lindex('primeList',1).decode('utf8')
            return cache.lrange('primeList',0,-1)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)



def set(value): #sets "chosenNumber" in redis with the number inputed in the url
    retries = 5
    while True:
        try:
            return cache.set(chosenNumber,value)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get(): #gets the "chosenNumber" from redis
    retries = 5
    while True:
        try:
            return cache.get(chosenNumber).decode('utf8') #decodes byte string
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def decode(l):	#only return the value of the int and not a byte string
    if isinstance(l, list):
        return [decode(x) for x in l]
    else:
        return l.decode('utf-8')


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello to the Docker World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/reset') #This will reset the list of primes that are stored
def resetList():
    cache.delete('primeList')
    return 'List has been reset'

@app.route('/primesStored') #returns the stored primes
def primesStored():
	l = cache.lrange('primeList',0,-1)
	_decode = decode(l)
	primesStored = 'Primes Stored: {}'.format(_decode)
	return primesStored

@app.route('/isPrime/<int:number>') #checks if the number inputed is a prime
def show_prime_number(number):
	_number = number
	count = get_hit_count()
	_set = set(number) #sets the number inputed
	_get = get() #gets the number inputed
	
	
	#The following prime number checker is obtained and modified from https://www.geeksforgeeks.org/python-program-to-check-whether-a-number-is-prime-or-not/
		
	if (number<= 1):
		return '{} is not a prime number'.format(_number)
	if (number<=3):
		_lpush = lpush(_get) #adds to stored prime number list
		_lrange = lrange()
		return '{} is a prime number'.format(_number)
	if (number % 2 == 0 or number % 3 == 0):
		return '{} is not a prime number'.format(_number)

	i = 5
	while(i * i <= number):
		if (number % i == 0 or number % (i + 2) == 0):
			return '{} is not a prime number'.format(_number)
		i = i + 6
	_lpush = lpush(_get) #adds to stored prime number list
	_lrange = lrange()
	return '{} is a prime number'.format(_number)





