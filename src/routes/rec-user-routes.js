const RecUserController = require('../controllers/RecUserController');

const routes = app => {
  app.get('/rec/user', RecUserController.sendRecommendationsByUser);
};

module.exports = routes;
