const model = require('../models/model');
const express = require('express');

const app = express();


exports.analyze = async (req, res, next) => {

    const {
        book_name,
        character_name
    } = req.body;

    console.log(book_name);

    if (!book_name || !character_name) {
        return await res.status(400).send({
            message: "입력되지 않은 값 존재"
        });
    }

    // model 에서 받아와 view로 전송
    try {
        const { code, json } = await model.analyze(book_name, character_name)
        return res.status(code).send(json);
    } catch (err) {
        console.log(err);
        return await res.status(400).send({
            message: "test"
        });
    }
}