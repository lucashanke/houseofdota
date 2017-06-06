import React from 'react';
import LineUp from './LineUp.jsx';
import Recommended from './Recommended.jsx';

import ContentHolder from '../../components/ContentHolder.jsx';
import $ from 'jquery';

import { Toolbar, ToolbarGroup, ToolbarTitle,
  ToolbarSeparator, FontIcon, AutoComplete, MenuItem, DropDownMenu, RaisedButton } from 'material-ui';
import StatisticsService from '../../statistics/services/StatisticsService.js';

const initialState = {
  selectedAllies: [],
  selectedEnemies: [],
  heroes: [],
  team: 'radiant',
  searchAlly: '',
  searchEnemy: '',
  recommendedAllies: null,
  recommendedCounters: null,
}

export default class Recommendation extends React.Component {

  constructor(props) {
    super(props);
    this.statisticsService = new StatisticsService();
    this.state = initialState;
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
    this.setState({ recommendedAllies: [] })
    $.when(
      this.statisticsService.fetchHeroesStatisticsRecommendation(this.state.selectedAllies)
    ).done(response => {
      this.setState({ recommendedAllies: this.getAllies(response.statistics) })
    });
  }

  fetchCounterPicks() {
    this.setState({ recommendedCounters: [] })
    $.when(
      this.statisticsService.fetchEnemiesCounterStatistics(this.state.selectedEnemies)
    ).done(response => {
      this.setState({
        recommendedCounters: this.getCounters(response.results),
      })
    });
  }

  getRecommendation() {
    if(this.state.selectedAllies.length > 0 && this.state.selectedAllies.length < 5 )
      this.fetchBundleRecommendation();
    if(this.state.selectedEnemies.length > 0 && this.state.selectedAllies.length < 5)
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
    const unavailableCounters = this.getUnavailableHeroes();
    let selectedCounters = [];
    for (let i = 0; i < counters.length; i++){
      const counterId = counters[i].id;
      if(!unavailableCounters.includes(counterId)) {
        if(!selectedCounters.map(s => s.id).includes(counterId)) {
          selectedCounters.push({
            id: counters[i].id,
            name: counters[i].name,
            counterFor: 1,
          });
        } else {
          selectedCounters.filter(c => c.id === counterId)[0].counterFor++;
        }
      }
    }
    return selectedCounters.slice(0,5);
  }

  getAllies(bundles) {
    const orderedBundles = _.orderBy(bundles, ['bundleSize','confidence'], ['desc', 'desc']);
    const unavailableAllies = this.getUnavailableHeroes();
    let selectedRecommended = [];
    for (let i = 0; i < orderedBundles.length && selectedRecommended.length < 5; i++){
      const recommendedId = orderedBundles[i].recommended[0].id;
      if(!unavailableAllies.includes(recommendedId)
        && !selectedRecommended.map(s => s.id).includes(recommendedId)) {
          selectedRecommended.push({
            id: orderedBundles[i].recommended[0].id,
            name: orderedBundles[i].recommended[0].name,
            bundleSize: orderedBundles[i].bundleSize,
          });
      }
    }
    return selectedRecommended;
  }

  selectAlly(chosen, index) {
    const hero = this.state.heroes.filter((h) => h.heroId === chosen.valueKey);
    this.setState({
      heroes: this.state.heroes.filter((h) => h.heroId !== chosen.valueKey),
      selectedAllies: this.state.selectedAllies.concat(hero),
      searchAlly: '',
    });
  }

  reset() {
    this.setState(initialState);
    this.fetchHeroesList();
  }

  handleTapOfRecommended(heroId) {
    const hero = this.state.heroes.filter((h) => h.heroId === heroId);
    this.setState({
      heroes: this.state.heroes.filter((h) => h.heroId !== heroId),
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

  unselectHero(heroId) {
    const hero = this.state.selectedAllies.filter((h) => h.heroId === heroId).concat(
      this.state.selectedEnemies.filter((h) => h.heroId === heroId)
    );
    this.setState({
      heroes: this.state.heroes.concat(hero),
      selectedEnemies: this.state.selectedEnemies.filter((h) => h.heroId !== heroId),
      selectedAllies: this.state.selectedAllies.filter((h) => h.heroId !== heroId),
      searchAlly: '',
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
    if (this.state.recommendedAllies) {
      recommendedAllies = (
        <ContentHolder style={{width: '42.5%', marginRight: '2.5%'}}>
          <Toolbar>
            <ToolbarTitle text="Recommended based on Allies"/>
          </Toolbar>
          <Recommended
            recommended={this.state.recommendedAllies}
            onPickAction={this.handleTapOfRecommended.bind(this)}
          />
        </ContentHolder>
      );
    }

    let recommendedCounters = null;
    if (this.state.recommendedCounters) {
      recommendedCounters = (
        <ContentHolder style={{width: '42.5%', marginLeft: '2.5%', float: 'right'}}>
          <Toolbar>
            <ToolbarTitle text="Recommended based on Enemies"/>
          </Toolbar>
          <Recommended
            recommended={this.state.recommendedCounters}
            onPickAction={this.handleTapOfRecommended.bind(this)}
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
          onAction={this.unselectHero.bind(this)}
        />
        <Toolbar style={{backgroundColor: '#37474F'}}>
          <ToolbarGroup style={{ marginLeft: '36.5%' }}>
            <RaisedButton
              onTouchTap={this.getRecommendation.bind(this)}
              label="Recommend me some heroes!"
              disabled={this.state.selectedAllies.length === 0 && this.state.selectedEnemies.length === 0}
              secondary
              title="Select heroes and get recommendations!"
            />
          </ToolbarGroup>
          <ToolbarGroup>
            <RaisedButton
              onTouchTap={this.reset.bind(this)}
              label="Reset"
              backgroundColor="#263238"
              labelColor="white"
            />
          </ToolbarGroup>
        </Toolbar>
      </ContentHolder>
      {recommendedAllies}
      {recommendedCounters}
    </div>
    );
  }
}
