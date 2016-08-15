import React from 'react';
import ContentHolder from '../../components/ContentHolder.jsx';
import NNPerformanceWidget from  './NNPerformanceWidget.jsx';

export default class NNPerformance extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    return(
      <ContentHolder>
        <NNPerformanceWidget />
      </ContentHolder>
    );
  }
}
