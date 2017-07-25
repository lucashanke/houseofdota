export const getCounters = (results, unavailableHeroes) => {
  let counters = results.reduce((allCounters, heroCounter) => {
    return allCounters.concat(heroCounter.counterPicks);
  }, [])
  counters = _.orderBy( counters ,['counterCoefficient'], ['desc']);
  let selectedCounters = [];
  for (let i = 0; i < counters.length; i++){
    const counterId = counters[i].id;
    if(!unavailableHeroes.includes(counterId)) {
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

export const getAllies = (bundles, unavailableHeroes) => {
  const orderedBundles = _.orderBy(bundles, ['bundleSize','confidence'], ['desc', 'desc']);
  let selectedRecommended = [];
  for (let i = 0; i < orderedBundles.length && selectedRecommended.length < 5; i++){
    const recommendedId = orderedBundles[i].recommended[0].id;
    if(!unavailableHeroes.includes(recommendedId)
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
