const express = require('express');
const ejs = require('ejs');
const app = express();
const port = 3000;

const path = require("path");

app.get('/', (req, res, next) => {
    res.render('index', {
        title: 'Hello EJS'
    });
});

// body parser 
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.listen(port, () => console.log('Example app listening at'));

// 라우터 경로
app.use('/', require('./routes/index'));
app.use('/upload', express.static('uploads'));

// ejs로 뷰 엔진 변경 및 css 사용
app.use(express.static(__dirname + '/views'));
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(__dirname + '/public'));
app.use('/books', express.static(__dirname + '/public'));
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

module.exports = app;

