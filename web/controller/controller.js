const model = require('../models/model');
const express = require('express');
const app = express();

exports.analyze = async (req, res, next) => {

    console.log(req.body);
    const {
        tmp,
        character_name,
    } = req.body;

    // 텍스트 파일 객체
    let file = req.file
    console.log(file.filename)

    // model.js 호출하고 결과 view에 적용
    try {
        var data = await model.analyze(file.filename, character_name);

        data = data.join('\n');

        console.log(data);
        res.render('index', { success: data });
    } catch (err) {
        console.log(err);
        return res.render('index', { err: "오류" });
    }
}

