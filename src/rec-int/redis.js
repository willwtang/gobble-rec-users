const redis = require('redis');
const Promise = require('bluebird');
Promise.promisifyAll(redis.RedisClient.prototype);
Promise.promisifyAll(redis.Multi.prototype);

const connectToRedis = function() {
  const client = redis.createClient();
  return key => client.select(1).then(() => client.getAsync(key).then(res => JSON.parse(res)));
};

module.exports = connectToRedis();
