import redis

class RedisClient:
  def __init__(self):
    self.client = redis.StrictRedis(host='localhost', port=6379, db=0)

  def setJSON(self, json):
    print
    for key, value in json.items():
      self.client.set(key, value)

  def clear(self):
    self.client.flushdb()

  def get(self, key):
    return self.client.get(key)
