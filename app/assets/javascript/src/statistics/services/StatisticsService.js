import $ from 'jquery';

export default class StatisticsService {

  fetchHeroesStatistics(){
    return $.getJSON('/statistics/heroes');
  }

}
