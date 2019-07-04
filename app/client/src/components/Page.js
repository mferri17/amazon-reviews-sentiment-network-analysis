import React, { useState, useCallback } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Dataset from './Dataset/';
import Sentiment from './Sentiment/';

const LinkTab = props => (
  <Tab
    component="a"
    onClick={event => {
      event.preventDefault();
    }}
    {...props}
  />
);

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
  tabContainer: {
    maxHeight: 'calc(100vh - 112px)',
    height: 'calc(100vh - 112px)',
    width: '100vw',
    maxWidth: '100%',
    display: 'flex',
    flexDirection: 'row',
    overflow: 'auto'
  }
}));

const TeamTabs = () => {
  const classes = useStyles();
  const [value, setValue] = useState(0);

  const handleChange = useCallback((_, newValue) => {
    setValue(newValue);
  }, [setValue]);

  return (
    <div className={classes.root}>
      <AppBar position="static" elevation={0}>
        <Tabs variant="fullWidth" value={value} onChange={handleChange}>
          <LinkTab label="ABSA" href="/absa" />
          <LinkTab label="Sentiment" href="/sentiment" />
          <LinkTab label="Collaborative filtering" href="/collaborative-filtering" />
        </Tabs>
      </AppBar>
      <div className={classes.tabContainer}>
        {value === 0 && (
          <Dataset />
        )}
        {value === 1 && (
          <Sentiment />
        )}
      </div>
    </div>
  );
};

export default TeamTabs;
