const get = require('../rec-int/redis');
const fetch = require('isomorphic-fetch');
const gobbleDB = process.env.GOBBLE_DB_URL;

const getRecommendationsByUser = function(userId) {
  return get(userId)
    .then(res => {
      const upcs = res.map(upc => `upc=${upc}`).join('&');
      return fetch(`${gobbleDB}/db/recuser/product?${upcs}`).then(results => results.json());
    });
};

const sendRecommendationsByUser = function(req, res) {
  const userId = req.query.facebookId;
  getRecommendationsByUser(userId)
    .then(results => res.send(results))
    .catch(err => res.status(400).send(err));
};

module.exports = { sendRecommendationsByUser };
