import React from 'react';
import StatisticsService from '../services/StatisticsService.js';
import HeroesStatistics from './HeroesStatistics.jsx';
import HeroesStatisticsToolBar from './HeroesStatisticsToolBar.jsx';

import $ from 'jquery';

export default class HeroesStatisticsWidget extends React.Component {

  constructor(props){
    super(props);
    this.service = new StatisticsService();
    this.state = {
      matchQuantity: 0,
      statistics: [],
      orderBy: 'pickRate',
    }
  }

  componentWillMount(){
    $.when(
      this.service.fetchHeroesStatistics()
    ).done(result => {
      this.setState({
        matchQuantity: result.matchQuantity,
        statistics: result.statistics,
      });
    });
  }

  handleOrderChange(event, key, value){
    this.setState({
      orderBy: value,
    });
  }

  render(){
    return(
      <div>
        <HeroesStatisticsToolBar
          orderBy={ this.state.orderBy }
          matchQuantity={ this.state.matchQuantity }
          onOrderChange={ this.handleOrderChange.bind(this) } >
        </HeroesStatisticsToolBar>
        <HeroesStatistics
          statistics={ this.state.statistics }
          orderBy={ this.state.orderBy }/>
      </div>
    );
  }
}
