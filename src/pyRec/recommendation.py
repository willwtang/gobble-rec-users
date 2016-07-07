from numpy import dot, linalg, average, array
import heapq 
from math import trunc

class NLargest(list):
  def __init__(self, size):
    self.__size = size

  def add(self, element):
    if self.__size == len(self) and self[0] < element: 
      heapq.heapreplace(self, element)
      return

    heapq.heappush(self, element)

class Recommendation:
  def __init__(self, data, numRec, numNeigh):
    self.__data = data
    self.__numRec = numRec
    self.__numNeighbors = numNeigh

  def __cosDistance(self, vector1, vector2):
    preferences1 = array(vector1)
    preferences2 = array(vector2)
    result = dot(preferences1, preferences2) / (linalg.norm(preferences1) * linalg.norm(preferences2))
    return trunc(round(result, 4) * 10000) / 10000

  def __calculateDistances(self, user1, user2):
    vector1 = []
    vector2 = []
    currUserKeys = self.__data[user1].keys()
    for item in set().union(currUserKeys, self.__data[user2].keys()):
      if item in self.__data[user1]: vector1.append(self.__data[user1][item])
      else: vector1.append(0)

      if item in self.__data[user2]: vector2.append(self.__data[user2][item])
      else: vector2.append(0)

    distance = self.__cosDistance(vector1, vector2)
    return (distance, user2)

  def __neighbors(self, userId):
    distances = NLargest(self.__numNeighbors)
    minimum = -1
    for user in self.__data:
      if user == userId: continue
      pair = self.__calculateDistances(userId, user)
      distances.add(pair)
    return distances

  def __compare(self, user, neighbor, total, recommendations):
    distance, neighborId = neighbor
    weight = distance / total if total != 0 else 1 / self.__numNeighbors

    userItems = self.__data[user]
    neighborItems = self.__data[neighborId]
    for item in neighborItems:
      if item in userItems: continue
      if not item in recommendations: 
        recommendations[item] = trunc(neighborItems[item] * weight * 10000) / 10000
      else: 
        recommendations[item] = trunc((recommendations[item] + neighborItems[item] * weight) * 10000) / 10000

  def recommend(self, userId):
    neighbors = self.__neighbors(userId)
    total = sum(i for i, j in neighbors)

    recommendations = {}

    for neighbor in neighbors:
      self.__compare(userId, neighbor, total, recommendations)

    recList = [(recommendations[item], item) for item in recommendations]
    heapq.heapify(recList)
    return heapq.nlargest(self.__numRec, recList)
    return [rec[1] for rec in heapq.nlargest(self.__numRec, recList)]
      
  def allRecommendations(self):
    results = {}
    for user in self.__data:
      results[user] = self.recommend(user)
    return results
