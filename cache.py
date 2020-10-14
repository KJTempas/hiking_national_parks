import time
from datetime import datetime
import json
import sys
from pymemcache.client.base import Client
from pymemcache import serde


#pickle converts objects to binary (serializes and deserializes)
# cache is stored in binary
#connect to memcached client
memcache_client = Client('localhost', serde=serde.pickle_serde)

def add(cachable):  #identifier is the key
    memcache_client.set(cachable.identifier, cachable, expire = 3600) #3600sec = 1 hour

def fetch(identifier, cls):
    cached_object = memcache_client.get(identifier)
    return cached_object