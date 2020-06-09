var express = require('express');
var router = express.Router();
const controller = require('../controller/controller');

router.post('/analyze', controller.analyze);

module.exports = router;