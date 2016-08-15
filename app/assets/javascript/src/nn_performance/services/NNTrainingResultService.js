import $ from 'jquery';

export default class NNTrainingResultService {

  fetchResults(){
    return $.getJSON('/nn_results');
  }

}
