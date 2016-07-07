const redis = require('redis');
const Promise = require('bluebird');
Promise.promisifyAll(redis.RedisClient.prototype);
Promise.promisifyAll(redis.Multi.prototype);

const connectToRedis = function() {
  const client = redis.createClient();
  return key => client.get(key);
};

module.exports = connectToRedis();
