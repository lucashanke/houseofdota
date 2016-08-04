import React from 'react';
import ContentHolder from '../../components/ContentHolder.jsx';
import HeroesStatisticsWidget from './HeroesStatisticsWidget.jsx'

export default class Statistics extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    return(
      <ContentHolder>
        <HeroesStatisticsWidget />
      </ContentHolder>
    );
  }
}
