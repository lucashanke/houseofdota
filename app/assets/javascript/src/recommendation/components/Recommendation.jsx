import React from 'react';
import $ from 'jquery';
import _ from 'lodash';
import { Toolbar, ToolbarGroup, ToolbarTitle,
  ToolbarSeparator, FontIcon, AutoComplete, MenuItem, DropDownMenu, RaisedButton, Snackbar } from 'material-ui';

import ContentHolder from '../../components/ContentHolder.jsx';
import LineUp from './LineUp.jsx';
import Recommended from './Recommended.jsx';
import LineUpSelection from './LineUpSelection.jsx';
import StatisticsService from '../../statistics/services/StatisticsService.js';

const MAX_TEAM_SIZE = 5;

const initialState = {
  selectedAllies: [],
  selectedEnemies: [],
  heroes: [],
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

  requestBundleRecommendations() {
    if(this.state.selectedAllies.length > 0 && this.state.selectedAllies.length < 5 )
      this.fetchBundleRecommendation();
  }

  requestCounterRecommendations() {
    if(this.state.selectedEnemies.length > 0 && this.state.selectedAllies.length < 5)
      this.fetchCounterPicks();
  }

  getUnavailableHeroes() {
    return this.state.selectedAllies.concat(this.state.selectedEnemies).map(h => h.heroId);
  }

  fullLineUp() {
    return this.state.selectedAllies.length === MAX_TEAM_SIZE;
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
    }, () => {
      this.requestBundleRecommendations();
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
    }, () => {
      this.requestBundleRecommendations();
    });
  }

  selectEnemy(chosen, index) {
    const hero = this.state.heroes.filter((h) => h.heroId === chosen.valueKey);
    this.setState({
      heroes: this.state.heroes.filter((h) => h.heroId !== chosen.valueKey),
      selectedEnemies: this.state.selectedEnemies.concat(hero),
      searchEnemy: '',
    }, () => {
      this.requestCounterRecommendations();
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
    }, () => {
      this.requestBundleRecommendations();
      this.requestCounterRecommendations();
    });
  }

  recommendationWasFetched() {
    return this.state.recommendedCounters !== null && this.state.recommendedCounters.length > 0 &&
      this.state.recommendedAllies !== null && this.state.recommendedAllies.length > 0;
  }

  handleActionTouchTap() {
    let win = window.open('https://goo.gl/forms/UACzHRdfrBxqp4MS2', '_blank');
    win.focus();
  }

  render() {
    let recommendedAllies = null;
    if (this.state.recommendedAllies && !this.fullLineUp()) {
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
    if (this.state.recommendedCounters && !this.fullLineUp()) {
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
        <LineUpSelection
          disableAllySelection={this.state.selectedAllies.length === MAX_TEAM_SIZE}
          disableEnemySelection={this.state.selectedEnemies.length === MAX_TEAM_SIZE}
          availableHeroes={this.state.heroes}
          onAllySelection={this.selectAlly.bind(this)}
          onEnemySelection={this.selectEnemy.bind(this)}
        />
        <LineUp
          allies={this.state.selectedAllies}
          enemies={this.state.selectedEnemies}
          onAction={this.unselectHero.bind(this)}
        />
        <Toolbar style={{backgroundColor: '#37474F'}}>
          <ToolbarGroup>
            <RaisedButton
              onTouchTap={this.reset.bind(this)}
              label="Reset"
              className="reset-button"
              backgroundColor="#263238"
              labelColor="#fff"
            />
          </ToolbarGroup>
        </Toolbar>
      </ContentHolder>
      {recommendedAllies}
      {recommendedCounters}
      <ContentHolder>
        <Snackbar
          open={this.recommendationWasFetched() || this.fullLineUp()}
          message="Used the recommendation? How do you feel about giving us some help?"
          autoHideDuration={7200000}
          action="I'm in!"
          onActionTouchTap={this.handleActionTouchTap}
        />
      </ContentHolder>
    </div>
    );
  }
}
