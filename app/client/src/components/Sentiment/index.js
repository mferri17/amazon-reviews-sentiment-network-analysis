import React, { useState, useCallback } from 'react';
import classnames from 'classnames';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import Absa from '../Absa';
import { getURL } from '../../utils';

const isPositive = ([negative, positive]) => positive >= negative;
const getPerc = ([negative, positive]) => Math.round(
  (positive > negative ? positive : negative) * 10000
) / 100;

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    width: '100%',
    flexDirection: 'row'
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1)
  },
  firstColumn: {
    width: '40%',
    display: 'flex',
    flexDirection: 'column'
  },
  secondColumn: {
    width: 'calc(60% - 32px)',
    display: 'flex',
    flexDirection: 'column',
    paddingTop: 16,
    paddingLeft: 16
  },
  button: {
    margin: theme.spacing(1),
  },
  dense: {
    marginTop: theme.spacing(2),
  },
  negative: {
    color: '#F44336'
  },
  positive: {
    color: '#4CAF50'
  },
  progress: {
    position: 'absolute',
    top: '50%',
    left: '50%',
		marginTop: '-20px',
		marginLeft: '-20px'
  },
  absaContainer: {
    marginTop: 24
  }
}));

const Sentiment = () => {
  const classes = useStyles();
  const [loading, setLoading] = useState(null);
  const [review, setReview] = useState(null);
  const [result, setResult] = useState(null);

  const {
    overall,
    absa
  } = result || {};

  const evaluate = useCallback(async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch(getURL('sentiment'), {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: review
        })
      });
      const result = await response.json();
      setResult(result);
    } catch (ex) {
      // TODO
    }
    setLoading(false);
  });

  return (
    <div className={classes.root}>
      <div className={classes.firstColumn}>
        <TextField
          label="Review"
          className={classnames(classes.textField, classes.dense)}
          margin="dense"
          variant="outlined"
          multiline
          rows="4"
          rowsMax="10"
          value={review}
          onChange={({ target: { value } }) => setReview(value)}
        />
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={evaluate}
        >
          Evaluate
        </Button>
        {loading && (
          <CircularProgress className={classes.progress} color="secondary" />
        )}
      </div>
      {result && (
        <div className={classes.secondColumn}>
          <Typography variant="h4">
            Overall sentiment
          </Typography>
          <Typography variant="h5">
            <span className={classnames({
              [classes.positive]: isPositive(overall),
              [classes.negative]: !isPositive(overall)
            })}>
              {isPositive(overall) ? 'Positive'  :'Negative'}
            </span>
            <span>
              {' '}with confidence {getPerc(overall)}%
            </span>
          </Typography>
          <div className={classes.absaContainer}>
            <Absa aspects={absa} />
          </div>
        </div>
      )}
    </div>
  );
};

export default Sentiment;