const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const express = require('express');
const bodyParser = require('body-parser');

const pythonSentimentPath = path.relative(__dirname, path.join(__dirname, 'predict.py'));
const pythonABSAPath = path.relative(__dirname, path.join(__dirname, '..', '..', 'scripts', 'aspect_sentiment.py'));
const tempFile = path.relative(__dirname, path.join(__dirname, 'temp.json'));

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
  const review = req.body.text.replace(/"/g, '');

  Promise.all([
    new Promise((resolve, reject) => {
      exec(`python ${pythonSentimentPath} "${review}"`, (err, stdout) => {
        if (err) {
          reject(err);
        } else {
          resolve(JSON.parse(stdout));
        }
      });
    }),
    new Promise((resolve, reject) => {
      exec(`python ${pythonABSAPath} --source "${review}" --threshold 0 --out ${tempFile}`, (err, stdout) => {
        if (err) {
          reject(err);
        } else {
          setTimeout(() => {
            const absa = JSON.parse(fs.readFileSync(tempFile, 'utf8'));
            fs.unlinkSync(tempFile);
            resolve(absa);
          }, 300);
        }
      });
    })
  ])
    .then(([probs, absa]) => {
      res.json({
        overall: probs,
        absa
      });
    })
    .catch(ex => {
      res.status(500).json(ex);
    });
});

app.listen(1234, function () {
  console.log('Server listening on port 1234!');
});
