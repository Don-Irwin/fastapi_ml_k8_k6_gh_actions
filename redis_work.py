import redis 
from datetime import timedelta
import os

cache_hit = 0

redis_host = os.environ.get("REDIS_SERVER","redis")
print(redis_host)


min = 1
max = 100
n = 20000
r = redis.Redis(host="localhost", port=6379, db=0)

import numpy as np
keys = np.random.randint(min,max,n)

# for key in range(min,max+1):
#     r.setex(int(key),timedelta(minutes=1),value="cached")

#print(r.keys())

#print(keys)

for i, key in enumerate(keys):
    my_key = int(str(key))
    #print(key)
    if r.get(my_key):
        cache_hit += 1
    else:
        r.setex(my_key,timedelta(minutes=1),value="cached")
    if i % 100 == 0:
        print(i,cache_hit / (i+1))
