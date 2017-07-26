import React from 'react';
import $ from 'jquery';
import _ from 'lodash';
import { Toolbar, ToolbarGroup, ToolbarTitle,
  ToolbarSeparator, FontIcon, AutoComplete, MenuItem, DropDownMenu, RaisedButton, Snackbar } from 'material-ui';

import ContentHolder from '../../components/ContentHolder.jsx';
import LineUp from './LineUp.jsx';
import LineUpSelection from './LineUpSelection.jsx';
import Recommended from './Recommended.jsx';
import { getAllies, getCounters } from '../recommendation.js';
import StatisticsService from '../../statistics/services/StatisticsService.js';

const MAX_TEAM_SIZE = 5;

const initialState = {
  selectedAllies: [],
  selectedEnemies: [],
  heroes: [],
  recommendedAllies: null,
  recommendedCounters: null,
};

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
      this.setState({
        recommendedAllies: getAllies(response.statistics, this.getUnavailableHeroes())
      });
    });
  }

  fetchCounterPicks() {
    this.setState({ recommendedCounters: [] })
    $.when(
      this.statisticsService.fetchEnemiesCounterStatistics(this.state.selectedEnemies)
    ).done(response => {
      this.setState({
        recommendedCounters: getCounters(response.results, this.getUnavailableHeroes()),
      });
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

  selectAlly(heroId) {
    const hero = this.state.heroes.filter((h) => h.heroId === heroId);
    this.setState({
      heroes: this.state.heroes.filter((h) => h.heroId !== heroId),
      selectedAllies: this.state.selectedAllies.concat(hero),
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
    }, () => {
      this.requestBundleRecommendations();
    });
  }

  selectEnemy(heroId) {
    const hero = this.state.heroes.filter((h) => h.heroId === heroId);
    this.setState({
      heroes: this.state.heroes.filter((h) => h.heroId !== heroId),
      selectedEnemies: this.state.selectedEnemies.concat(hero),
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
      <Recommended
        recommendedAllies={this.state.recommendedAllies}
        recommendedCounters={this.state.recommendedCounters}
        onTapOfRecommended={this.handleTapOfRecommended.bind(this)}
        fullLineUp={this.fullLineUp()}
      />
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
