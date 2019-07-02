import React from 'react';
import classnames from 'classnames';
import { makeStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

const getMostFrequentPolarity = ({ positive, negative, neutral }) => {
  const percents = [positive, negative, neutral].map(x => x.percent);
  
  switch (Math.max(...percents)) {
    case positive.percent:
      return 'positive';
    case negative.percent:
      return 'negative';
    default:
      return 'neutral';
  }
};
const getAspectName = aspect => aspect || 'Overall';
const getPolarityName = ([firstLetter, ...others]) => `${firstLetter.toUpperCase()}${others.join('')}`;

const useStyles = makeStyles(theme => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: 'bold',
    flexBasis: '33.33%',
    flexShrink: 0,
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
  bold: {
    fontWeight: 'bold'
  },
  negative: {
    color: '#F44336'
  },
  positive: {
    color: '#4CAF50'
  },
  column: {
    display: 'flex',
    flexDirection: 'column'
  },
  polarityDetail: {
    marginBottom: 16
  }
}));

const Absa = ({ aspects }) => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      {Object.keys(aspects).map(aspectStr => {
        const aspect = aspects[aspectStr];
        const mostFrequent = getMostFrequentPolarity(aspect);
        const polarityClasses = {
          [classes.positive]: mostFrequent === 'positive',
          [classes.negative]: mostFrequent === 'negative'
        };

        return (
          <ExpansionPanel key={aspectStr}>
            <ExpansionPanelSummary
              expandIcon={<ExpandMoreIcon />}
            >
              <Typography className={classes.heading}>{getAspectName(aspectStr)}</Typography>
              <Typography className={classes.secondaryHeading}>
              <span
                className={classnames({
                  [classes.bold]: true,
                  ...polarityClasses
                })}
              >
                {getPolarityName(mostFrequent)}
              </span> - score {aspect[mostFrequent].score} - sentences {aspect[mostFrequent].percent}%</Typography>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
              <div className={classes.column}>
                {Object.keys(aspect).map(x => (
                  <div className={classes.polarityDetail}>
                    <Typography>
                      <span
                        className={classnames(classes.bold, classes[x])}
                      >
                        {getPolarityName(x)}
                      </span> - score {aspect[x].score} - sentences {aspect[x].percent}%
                    </Typography>
                    <Typography>
                      <span className={classes.bold}>Adjectives</span>: {aspect[x].adjectives.join(', ') || '-'}
                    </Typography>
                    <Typography>
                      <span className={classes.bold}>Sentences</span>:
                    </Typography>
                    {aspect[x].sentences.map(sentence => (
                      <Typography>
                        {sentence}
                      </Typography>
                    )) || '-'}
                  </div>
                ))}
              </div>
            </ExpansionPanelDetails>
          </ExpansionPanel>
        );
      })}
    </div>
  );
};

export default Absa;