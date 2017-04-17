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
      bundleSize: 1,
    };
    this.updateStatistics.bind(this);
  }

  componentWillMount(){
    this.updateStatistics(this.state.bundleSize);
  }

  updateStatistics(bundleSize){
    $.when(
      this.service.fetchHeroesStatistics(bundleSize)
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

  handleBundleSizeChange(event, key, value){
    this.setState({
      bundleSize: value,
    });
    this.updateStatistics(value);
  }

  render(){
    return(
      <div>
        <HeroesStatisticsToolBar
          orderBy={ this.state.orderBy }
          bundleSize={ this.state.bundleSize }
          matchQuantity={ this.state.matchQuantity }
          onOrderChange={ this.handleOrderChange.bind(this) }
          onBundleSizeChange={ this.handleBundleSizeChange.bind(this) }>
        </HeroesStatisticsToolBar>
        <HeroesStatistics
          statistics={ this.state.statistics }
          orderBy={ this.state.orderBy }/>
      </div>
    );
  }
}
