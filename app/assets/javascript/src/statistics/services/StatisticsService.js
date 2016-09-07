import $ from 'jquery';

export default class StatisticsService {

  fetchHeroesStatistics(bundleSize){
    return $.getJSON('/statistics/heroes?bundle_size='+bundleSize);
  }

  fetchCounterStatistics(heroId){
    return $.getJSON('/statistics/counter?hero_id='+heroId);
  }

  fetchHeroes(){
    return $.getJSON('/heroes');
  }

}
