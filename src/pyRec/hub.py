from sys import argv
from json import dumps, loads

from recommendation import Recommendation
from redisConnect import RedisClient

client = RedisClient()

class ProcessRecs:
  @staticmethod
  def recommend(data):
    recs = Recommendation(data, 5, 5)
    return (recs.allRecommendations())

  @staticmethod
  def parseJSON(stringifiedJSON):
    data = loads(stringifiedJSON)
    parsed = {}
    for rating in data:
      # print (rating)
      user = rating['User_facebook_id']
      parsed[user] = parsed.get(user, {})
      parsed[user][rating['Product_upc']] = rating['rating']
    return parsed

  @staticmethod
  def store(json):
    client.setJSON(json)

  @staticmethod
  def get(key):
    return client.get(key)

  @staticmethod
  def hub():
    raw = argv[1]
    parsed = ProcessRecs.parseJSON(raw)
    rec = ProcessRecs.recommend(parsed)
    ProcessRecs.store(rec)

ProcessRecs.hub()



# data = loads(argv[1])
# print (dumps(recommend(data)))
# data = loads(data)
# b = ProcessRecs.recommend({
#   "Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
#   "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
#   "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
#   "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
#   "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
#   "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
#   "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
#   "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
# })
# print(b)

