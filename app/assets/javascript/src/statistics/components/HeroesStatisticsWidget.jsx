import React from 'react';
import StatisticsService from '../services/StatisticsService.js';
import HeroesStatistics from './HeroesStatistics.jsx';
import $ from 'jquery';

export default class HeroesStatisticsWidget extends React.Component {

  constructor(props){
    super(props);
    this.service = new StatisticsService();
    this.state = {
      matchQuantity: 0,
      statistics: [],
    }
  }

  componentWillMount(){
    $.when(
      this.service.fetchHeroesStatistics()
    ).done(result => {
      this.setState({
        matchQuantity: result.match_quantity,
        statistics: result.statistics,
      });
    });
  }

  render(){
    return(
      <HeroesStatistics
        matchQuantity={ this.state.matchQuantity }
        statistics={ this.state.statistics }/>
    );
  }
}
