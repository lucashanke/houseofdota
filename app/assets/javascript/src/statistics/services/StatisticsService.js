import $ from 'jquery';

export default class StatisticsService {

  fetchHeroesStatistics(bundleSize){
    return $.getJSON('/statistics/heroes?bundle_size='+bundleSize);
  }

}
