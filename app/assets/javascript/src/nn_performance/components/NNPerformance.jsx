import React from 'react';
import NNPerformanceWidget from  './NNPerformanceWidget.jsx';

export default class NNPerformance extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    return(
        <NNPerformanceWidget />
    );
  }
}
