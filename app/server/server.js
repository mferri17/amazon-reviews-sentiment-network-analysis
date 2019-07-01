const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');

const rScriptPath = path.relative(__dirname, path.join(__dirname, '..', 'R-scripts', 'ui_predict.R'));
const rInferencePath = path.relative(__dirname, path.join(__dirname, '..', 'R-scripts', 'ui_inference.R'));
const jsonPath = path.relative(__dirname, path.join(__dirname, '..', 'R-scripts', 'tempData.json'));

const dbDir = path.join(__dirname, '..', 'dataset');
const dbFile = path.join(dbDir, 'database.sqlite');
const connectDb = () => new sqlite3.Database(dbFile);

const toFixed2 = n => Math.round(n * 100) / 100;

const app = express();
app.use(bodyParser.urlencoded({
  extended: false
}));
app.use(bodyParser.json());

app.use((_, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

app.post('/inference', (req, res) => {
  const evidence = Object.keys(req.body).reduce((acc, cur) => ({
    ...acc,
    [cur]: req.body[cur] || undefined
  }), {});

  fs.writeFileSync(jsonPath, JSON.stringify(evidence));

  exec(`Rscript ${rInferencePath}`, (err, stdout) => {
    if (err) {
      res.status(500).json(err);
    } else {
      const out = stdout.split(/\r?\n/);
      const perc = Number(out[out.length - 1]);
      res.json(perc);
    }
  });
});

app.listen(1234, function () {
  console.log('Server listening on port 1234!');
});
