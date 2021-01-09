const model = require('../models/model');
const express = require('express');
const app = express();

exports.analyze = async (req, res, next) => {

    console.log(req.body);
    const {
        tmp,
        character_name,
    } = req.body;

    if (!req.file) {
        return res.render('index', { err: "파일을 입력해주세요" });
    }

    if (!character_name) {
        return res.render('index', { err: "등장인물을 입력해주세요" });
    }

    // 텍스트 파일 객체
    let file = req.file
    console.log(file.filename);
    console.log(character_name);
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

