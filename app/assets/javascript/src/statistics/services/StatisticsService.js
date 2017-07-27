import axios from 'axios';

export default class StatisticsService {

  fetchHeroesStatistics(bundleSize){
    return axios.get('/statistics/heroes?bundle_size='+bundleSize);
  }

  fetchHeroesStatisticsRecommendation(heroes){
    return axios.get(
      '/recommendation/bundles/?hero_ids[]=' +
        heroes.map(h => h.heroId.toString()).join(',')
    );
  }

  fetchCounterStatistics(heroId){
    return axios.get('/recommendation/counters?hero_ids[]='+heroId);
  }

  fetchEnemiesCounterStatistics(heroes){
    return axios.get('/recommendation/counters?hero_ids[]=' +
      heroes.map(h => h.heroId.toString()).join(','));
  }

  fetchExperiment(){
    return axios.get('/experiments/random');
  }

  fetchHeroes(){
    return axios.get('/heroes');
  }

}
