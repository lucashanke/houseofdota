import React from 'react';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import ShowChart from 'material-ui/svg-icons/editor/show-chart';
import { LineChart } from 'rd3';
import * as d3 from "d3";
import _ from 'lodash';

export default class NNPerformanceHistory extends React.Component {

  constructor(props){
    super(props);
    this.buildChart = this.buildChart.bind(this);
    this.buildChartData = this.buildChartData.bind(this);
    this.getTimeDomain = this.getTimeDomain.bind(this);
  }

  buildChart(){
    if (this.props.results.length > 0){
      return (
        <LineChart
          legend={true}
          data={ this.buildChartData() }
          width='100%'
          height={400}
          viewBoxObject={{
            x: 0,
            y: 0,
            width: 400,
            height: 400
          }}
          gridHorizontal={true}
          yAxisLabel='Accuracy (%)'
          xAxisLabel='Training Date'
          xAxisTickInterval={{unit: 'day', interval: 1}}
          />
      );
    }
    return (
      <span>No data to be displayed.</span>
    );
  }

  buildChartData(){
    return [
      {
        name: 'Testing',
        values: this.props.results.map((result) => {
          return {
            x: new Date(result.startTime),
            y: result.testingAccuracy
          };
        })
      },
      {
          name: 'Training',
          values: this.props.results.map((result) => {
            return {
              x: new Date(result.startTime),
              y: result.trainingAccuracy
            };
          })
      },
      {
        name: 'Baseline',
        values: this.props.results.map((result) => {
          return {
            x: new Date(result.startTime),
            y: result.radiantWinTestPercentage
          };
        })
      }
    ];
  }

  getTimeDomain(){
    const ordered = _.orderBy(this.props.results, 'startTime');
    return [new Date(ordered[0].startTime), new Date(ordered[ordered.length-1].startTime)];
  }

  render(){
    return (
      <Card style={{textAlign: 'left'}}>
        <CardHeader
          title="Performance History"
          avatar={<ShowChart />}/>
        <CardText>
          {  this.buildChart() }
        </CardText>
      </Card>
    );
  }
}

NNPerformanceHistory.propTypes = {
  results: React.PropTypes.array,
};
