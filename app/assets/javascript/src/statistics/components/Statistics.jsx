import React from 'react';
import HeroesStatisticsWidget from './HeroesStatisticsWidget.jsx'

export default class Statistics extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    return(
      <HeroesStatisticsWidget />
    );
  }
}
