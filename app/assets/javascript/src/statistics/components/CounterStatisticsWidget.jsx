import React from 'react';
import StatisticsService from '../services/StatisticsService.js';
import CounterStatisticsToolBar from './CounterStatisticsToolBar.jsx';
import CounterStatistics from './CounterStatistics.jsx';

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
      this.service.fetchCounterStatistics(heroId).then(result => {
        this.setState({
          heroId: heroId,
          matchQuantity: result.data.results[0].matchQuantity,
          counterPicks: result.data.results[0].counterPicks,
        });
      });
    }
  }

  getHeroesList(heroId){
    this.service.fetchHeroes().then(result => {
      this.setState({
        heroes: result.data.heroes,
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
