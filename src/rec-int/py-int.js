const PythonShell = require('python-shell');

const py = new PythonShell('recommendation.py', { mode: 'text', scriptPath: `${__dirname}/../pyRec/`, args: ['value1', 'value2'] });



