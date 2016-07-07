const fetch = require('isomorphic-fetch');
const gobbleDB = process.env.GOBBLE_DB_URL;
const pyConnect = require('./py-int');

const getReviewData = function() {
  fetch(`${gobbleDB}/db/recuser`)
    .then(res => res.json());
};

const runPythonScript = function(data) {
  pyConnect(data);
};

const updateRecs = setInterval(() => {
  getReviewData()
    .then(data => runPythonScript(data))
    .catch(err => console.log(err));
}, 86400);

module.exports = updateRecs;
