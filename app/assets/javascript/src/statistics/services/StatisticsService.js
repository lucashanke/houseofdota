import $ from 'jquery';

export default class StatisticsService {

  fetchHeroesStatistics(bundleSize){
    return $.getJSON('/statistics/heroes?bundle_size='+bundleSize);
  }

  fetchHeroesStatisticsRecommendation(heroes){
    return $.getJSON(
      '/recommendation/bundles/?hero_ids[]=' +
        heroes.map(h => h.heroId.toString()).join(',')
    );
  }

  fetchCounterStatistics(heroId){
    return $.getJSON('/recommendation/counters?hero_ids[]='+heroId);
  }

  fetchEnemiesCounterStatistics(heroes){
    return $.getJSON('/recommendation/counters?hero_ids[]=' +
      heroes.map(h => h.heroId.toString()).join(','));
  }

  fetchExperiment(){
    return $.getJSON('/experiments/random');
  }

  fetchHeroes(){
    return $.getJSON('/heroes');
  }

}
