import React from 'react';
import LineUp from './LineUp.jsx';
import Recommended from './Recommended.jsx';

import ContentHolder from '../../components/ContentHolder.jsx';
import $ from 'jquery';

import { Toolbar, ToolbarGroup, ToolbarTitle,
  ToolbarSeparator, FontIcon, AutoComplete, MenuItem, DropDownMenu, RaisedButton } from 'material-ui';
import StatisticsService from '../../statistics/services/StatisticsService.js';

export default class Recommendation extends React.Component {

  constructor(props) {
    super(props);
    this.statisticsService = new StatisticsService();
    this.state = {
      selectedAllies: [],
      selectedEnemies: [],
      heroes: [],
      team: 'radiant',
      searchAlly: '',
      searchEnemy: '',
      recommendedAllies: [],
      recommendedCounters: [],
    };
  }

  componentWillMount() {
    this.fetchHeroesList();
  }

  fetchHeroesList() {
    $.when(
      this.statisticsService.fetchHeroes()
    ).done(result => {
      this.setState({
        heroes: result.heroes,
      });
    });
  }

  fetchBundleRecommendation() {
    $.when(
      this.statisticsService.fetchHeroesStatisticsRecommendation(this.state.selectedAllies)
    ).done(result => {
      const recommended = result.statistics.map(s => s.recommended[0]);
      this.setState({
        recommendedAllies: recommended.filter(r => !this.state.selectedEnemies.map(e => e.heroId).includes(r.id)).slice(0,5),
      });
    });
  }

  fetchCounterPicks() {
    $.when(
      this.statisticsService.fetchEnemiesCounterStatistics(this.state.selectedEnemies)
    ).done(response => {
      this.setState({
        recommendedCounters: this.getCounters(response.results),
      })
    });
  }

  getRecommendation() {
    this.fetchBundleRecommendation();
    this.fetchCounterPicks();
  }

  getUnavailableHeroes() {
    return this.state.selectedAllies.concat(this.state.selectedEnemies).map(h => h.heroId);
  }

  getCounters(results) {
    let counters = results.reduce((allCounters, heroCounter) => {
      return allCounters.concat(heroCounter.counterPicks);
    }, [])
    counters = _.orderBy( counters ,['counterCoefficient'], ['desc']);
    debugger;
    const unavailableCounters = this.getUnavailableHeroes();
    let selectedCounters = [];
    for (let i = 0; i < counters.length && selectedCounters.length < 5; i++){
      const counterId = counters[i].id;
      if(!unavailableCounters.includes(counterId)
        && !selectedCounters.map(s => s.heroId).includes(counterId)) {
          selectedCounters.push(counters[i]);
        }
    }
    return selectedCounters;
  }

  selectAlly(chosen, index) {
    const hero = this.state.heroes.filter((h) => h.heroId === chosen.valueKey);
    this.setState({
      heroes: this.state.heroes.filter((h) => h.heroId !== chosen.valueKey),
      selectedAllies: this.state.selectedAllies.concat(hero),
      searchAlly: '',
    });
  }

  selectEnemy(chosen, index) {
    const hero = this.state.heroes.filter((h) => h.heroId === chosen.valueKey);
    this.setState({
      heroes: this.state.heroes.filter((h) => h.heroId !== chosen.valueKey),
      selectedEnemies: this.state.selectedEnemies.concat(hero),
      searchEnemy: '',
    });
  }

  handleUpdateInputAlly(searchText) {
    this.setState({
      searchAlly: searchText,
    });
  };

  handleUpdateInputEnemy(searchText) {
    this.setState({
      searchEnemy: searchText,
    });
  };

  constructHeroesOptions() {
    if (this.state.heroes !== undefined) return this.state.heroes.map(hero => {
      return {
        valueKey: hero.heroId,
        text: hero.localizedName,
        value: (
          <MenuItem
            primaryText={ hero.localizedName } >
          </MenuItem>
        ),
      };
    });
    return [];
  }

  handleTeamChange(event, key, value){
    this.setState({
      team: value,
    });
  }

  render() {
    let recommendedAllies = null;
    if (this.state.recommendedAllies.length > 0) {
      recommendedAllies = (
        <ContentHolder style={{width: '42.5%', marginRight: '2.5%'}}>
          <Toolbar>
            <ToolbarTitle text="Recommended based on Allies"/>
          </Toolbar>
          <Recommended
            recommended={this.state.recommendedAllies}
          />
        </ContentHolder>
      );
    }

    let recommendedCounters = null;
    if (this.state.recommendedCounters.length > 0) {
      recommendedCounters = (
        <ContentHolder style={{width: '42.5%', marginLeft: '2.5%', float: 'right'}}>
          <Toolbar>
            <ToolbarTitle text="Recommended based on Enemies"/>
          </Toolbar>
          <Recommended
            recommended={this.state.recommendedCounters}
          />
        </ContentHolder>
      );
    }

    return (
      <div>
      <ContentHolder>
        <Toolbar>
          <ToolbarGroup>
            <FontIcon className="material-icons"
              style={{ marginRight: '0.5em' }}>person_pin</FontIcon>
            <AutoComplete
              filter={AutoComplete.fuzzyFilter}
              openOnFocus={true}
              dataSource={this.constructHeroesOptions()}
              hintText="Select an Ally"
              searchText={this.state.searchAlly}
              disabled={this.state.selectedAllies.length === 5}
              onUpdateInput={this.handleUpdateInputAlly.bind(this)}
              onNewRequest={this.selectAlly.bind(this)} />
            <ToolbarSeparator />
          </ToolbarGroup>
          <ToolbarTitle text="Line-Up Selection"/>
          <ToolbarGroup>
            <ToolbarSeparator />
            <FontIcon className="material-icons"
              style={{ marginRight: '0.5em' }}>person_pin</FontIcon>
            <AutoComplete
              filter={AutoComplete.fuzzyFilter}
              openOnFocus={true}
              dataSource={ this.constructHeroesOptions() }
              hintText="Select an Enemy"
              searchText={this.state.searchEnemy}
              disabled={this.state.selectedEnemies.length === 5}
              onUpdateInput={this.handleUpdateInputEnemy.bind(this)}
              onNewRequest={this.selectEnemy.bind(this)} />
          </ToolbarGroup>
        </Toolbar>
        <LineUp
          allies={this.state.selectedAllies}
          enemies={this.state.selectedEnemies}
        />
        <Toolbar>
          <ToolbarGroup>
            <ToolbarTitle text="Select your Team"/>
            <DropDownMenu
              value={this.state.team}
              onChange={this.handleTeamChange.bind(this)}
            >
              <MenuItem value={'radiant'} label="Team: Radiant" primaryText="Radiant" />
              <MenuItem value={'dire'} label="Team: Dire" primaryText="Dire" />
            </DropDownMenu>
          </ToolbarGroup>
          <ToolbarGroup>
            <RaisedButton
              onTouchTap={this.getRecommendation.bind(this)}
              label="Get Recommendations" primary={true}/>
          </ToolbarGroup>
        </Toolbar>
      </ContentHolder>
      {recommendedAllies}
      {recommendedCounters}
    </div>
    );
  }
}
