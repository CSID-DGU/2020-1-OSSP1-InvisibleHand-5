var fs = require('fs');

exports.analyze = async (book_name, character_name) => {

    // 텍스트 파일 read
    fs.exists(book_name, function (exists) {
        console.log(exists ? "it's there" : "no exists!");
    });

    var book_text = fs.readFileSync(book_name, 'utf8');

    console.log(book_text);

    // 파이썬 main.py 호출
    var PythonShell = require('python-shell');
    var options = {
        mode: 'text',
        pythonPath: '',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: [book_name, book_text, character_name]
    };


    PythonShell.PythonShell.run("../src_test/main.py", options, function (err, data) {
        if (err) throw err;
        console.log(data);
    });
}