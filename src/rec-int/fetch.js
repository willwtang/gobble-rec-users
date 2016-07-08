const fetch = require('isomorphic-fetch');
const gobbleDB = process.env.GOBBLE_DB_URL;
const pyConnect = require('./py-int');

const getReviewData = function() {
  return fetch(`${gobbleDB}/db/recuser`)
    .then(res => res.json());
};

const runPythonScript = function(data) {
  pyConnect(data);
};

const updateRecs = function() {
  getReviewData()
    .then(data => runPythonScript(data))
    .catch(err => console.log(err));
};

updateRecs();
setInterval(updateRecs, 88000);

module.exports = updateRecs;
