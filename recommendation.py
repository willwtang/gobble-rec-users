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
    preferences1 = array(vector1) - average(vector1)
    preferences2 = array(vector2) - average(vector2)
    result = dot(preferences1, preferences2) / (linalg.norm(preferences1) * linalg.norm(preferences2));
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
    weight = distance / total

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
      
  def allRecommendations(self):
    results = {}
    for user in self.__data:
      results[user] = self.recommend(user)
    return results


dataSet = {
"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
"Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
"Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
"Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
"Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
"Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
"Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
"Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
}

a = Recommendation(dataSet, 5, 3)
print (a.allRecommendations())





