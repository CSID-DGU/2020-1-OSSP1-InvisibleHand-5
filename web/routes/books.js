var express = require('express');
var router = express.Router();
const multer = require('multer');

const controller = require('../controller/controller');

// multer 미들웨어 등록
let upload = multer({
    dest: "upload/"
})

router.post('/analyze', upload.single("book"), controller.analyze);

module.exports = router;