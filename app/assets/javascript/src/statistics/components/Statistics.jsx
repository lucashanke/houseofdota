import React from 'react';
import { Tabs, Tab } from 'material-ui';

import HeroesStatisticsWidget from './HeroesStatisticsWidget.jsx';
import CounterStatisticsWidget from './CounterStatisticsWidget.jsx';
import ContentHolder from '../../components/ContentHolder.jsx';

export default class Statistics extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      widget: "statistics",
    }
  }

  handleChange(value) {
    this.setState({
      widget: value,
    })
  }

  render(){
    const widget = this.state.widget == 'statistics' ?
      <HeroesStatisticsWidget /> : <CounterStatisticsWidget /> ;
    return(
      <div>
        <ContentHolder>
          <Tabs
            value={this.state.widget}
            onChange={this.handleChange.bind(this)} >
            <Tab label="Hero Bundles" value="statistics" />
            <Tab label="Hero Counters" value="counters" />
          </Tabs>
        </ContentHolder>
        { widget }
      </div>
    );
  }
}
