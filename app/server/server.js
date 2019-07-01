const path = require('path');
const { exec } = require('child_process');
const express = require('express');
const bodyParser = require('body-parser');

const pythonSentimentPath = path.relative(__dirname, path.join(__dirname, 'predict.py'));

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

app.post('/sentiment', (req, res) => {
  exec(`python ${pythonSentimentPath} "${req.body.text.replace(/"/g, '')}"`, (err, stdout) => {
    if (err) {
      res.status(500).json(err);
    } else {
      res.json(
        stdout
          .replace('[\'', '')
          .replace('\']', '')
      );
    }
  });
});

app.listen(1234, function () {
  console.log('Server listening on port 1234!');
});
