// python-shell로  main.py 호출하여 결과 반환
module.exports = {
    analyze: async (book_name, character_name) => {

        var PythonShell = require('python-shell');
        var options = {
            mode: 'text',
            pythonPath: '',
            pythonOptions: ['-u'],
            scriptPath: '',
            args: [book_name, character_name]
        };

        // 파이썬 main.py 호출
        const data = await new Promise((resolve, reject) => {
            PythonShell.PythonShell.run("source/main.py", options, (err, data) => {
                if (err) return reject(err);
                return resolve(data);
            });
        });

        return data;
    }
}