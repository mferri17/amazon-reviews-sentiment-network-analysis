import React from 'react';
import Absa from '../Absa';
import aspectResult from './aspect_sentiment.json';

const Dataset = () => (
  <Absa aspects={aspectResult} />
);

export default Dataset;
