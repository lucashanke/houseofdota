import React from 'react';
import StatisticsService from '../services/StatisticsService.js';
import CounterStatisticsToolBar from './CounterStatisticsToolBar.jsx';
import CounterStatistics from './CounterStatistics.jsx';

import $ from 'jquery';

export default class HeroesStatisticsWidget extends React.Component {

  constructor(props){
    super(props);
    this.service = new StatisticsService();
    this.state = {
      heroId: null,
      matchQuantity: 0,
      counterPicks: [],
      orderBy: 'counterCoefficient',
      heroes: [],
    };
    this.updateCounterStatistics.bind(this);
    this.getHeroesList();
  }

  updateCounterStatistics(heroId){
    if (heroId != null){
      $.when(
        this.service.fetchCounterStatistics(heroId)
      ).done(result => {
        this.setState({
          heroId: heroId,
          matchQuantity: result.matchQuantity,
          counterPicks: result.counterPicks,
        });
      });
    }
  }

  getHeroesList(heroId){
    $.when(
      this.service.fetchHeroes()
    ).done(result => {
      this.setState({
        heroes: result.heroes,
      });
    });
  }

  handleOrderChange(event, key, value){
    this.setState({
      orderBy: value,
    });
  }

  handleHeroChange(chosen, index){
    this.updateCounterStatistics(chosen.valueKey);
  }

  render(){
    return(
      <div>
        <CounterStatisticsToolBar
          heroes={ this.state.heroes }
          orderBy={ this.state.orderBy }
          heroId={ this.state.heroId }
          matchQuantity={ this.state.matchQuantity }
          onOrderChange={ this.handleOrderChange.bind(this) }
          onHeroChange={ this.handleHeroChange.bind(this) } />
        <CounterStatistics
          counters={ this.state.counterPicks }
          orderBy={ this.state.orderBy }/>
      </div>
    );
  }
}
