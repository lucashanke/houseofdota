import $ from 'jquery';

export default class StatisticsService {

  fetchHeroesStatistics(bundleSize){
    return $.getJSON('/statistics/heroes?bundle_size='+bundleSize);
  }

  fetchHeroesStatisticsRecommendation(heroes){
    return $.getJSON(
      '/statistics/heroes/recommend/?hero_ids[]=' +
        heroes.map(h => h.heroId.toString()).join(',')
    );
  }

  fetchCounterStatistics(heroId){
    return $.getJSON('/statistics/counter?hero_ids[]='+heroId);
  }

  fetchEnemiesCounterStatistics(heroes){
    return $.getJSON('/statistics/counter?hero_ids[]=' +
      heroes.map(h => h.heroId.toString()).join(','));
  }

  fetchExperiment(){
    return $.getJSON('/experiments/random');
  }

  fetchHeroes(){
    return $.getJSON('/heroes');
  }

}
