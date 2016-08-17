import React from 'react';
import NNTrainingResultService from '../services/NNTrainingResultService.js';
import NNCurrentStatus from './NNCurrentStatus.jsx';
import NNPerformanceHistory from './NNPerformanceHistory.jsx';
import ContentHolder from '../../components/ContentHolder.jsx';

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
      <div>
        <ContentHolder style={{width: '42.5%', marginRight: '2.5%'}}>
          <NNCurrentStatus
            lastTrainingResult={ lastTrainingResult }/>
        </ContentHolder>
        <ContentHolder style={{width: '42.5%', marginLeft: '2.5%'}}>
            <NNPerformanceHistory
              results={ this.state.results }/>
        </ContentHolder>
      </div>
    );
  }
}
