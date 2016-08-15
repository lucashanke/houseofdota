import React from 'react';
import NNTrainingResultService from '../services/NNTrainingResultService.js';
import NNCurrentStatus from './NNCurrentStatus.jsx';

import $ from 'jquery';

export default class NNPerformanceWidget extends React.Component {

  constructor(props){
    super(props);
    this.service = new NNTrainingResultService();
    this.state = {
      results: [],
      count: 0
    }
  }

  componentWillMount(){
    $.when(
      this.service.fetchResults()
    ).done(result => {
      this.setState({
        results: result.results,
        count: result.count,
      });
    });
  }

  render(){
    const lastTrainingResult = this.state.results[0];
    return(
      <NNCurrentStatus
        lastTrainingResult={ lastTrainingResult }/>
    );
  }
}
