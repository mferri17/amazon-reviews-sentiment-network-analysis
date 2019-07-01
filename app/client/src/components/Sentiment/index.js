import React, { useState, useCallback } from 'react';
import classnames from 'classnames';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import { getURL } from '../../utils';

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
  button: {
    margin: theme.spacing(1),
  },
  dense: {
    marginTop: theme.spacing(2),
  }
}));

const Sentiment = () => {
  const classes = useStyles();
  const [loading, setLoading] = useState(null);
  const [review, setReview] = useState(null);
  const [result, setResult] = useState(null);

  const evaluate = useCallback(async () => {
    setLoading(true);
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
        {result}
      </div>
    </div>
  );
};

export default Sentiment;