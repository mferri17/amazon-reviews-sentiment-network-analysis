import React, { useState, useCallback } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
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
    minHeight: 'calc(100vh - 112px)',
    height: '100%',
    width: '100vw',
    maxWidth: '100%',
    display: 'flex',
    flexDirection: 'row'
  },
  tabContent: {
    padding: 24,
    width: 'calc(100% - 48px)'
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
          <LinkTab label="Dataset" href="/dataset" />
          <LinkTab label="Sentiment" href="/sentiment" />
          <LinkTab label="Network" href="/network" />
        </Tabs>
      </AppBar>
      <div className={classes.tabContainer}>
        {value === 1 && (
          <Sentiment />
        )}
      </div>
    </div>
  );
};

export default TeamTabs;
