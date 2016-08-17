import React from 'react';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';

import LinearProgress from 'material-ui/LinearProgress';
import Divider from 'material-ui/Divider';
import DeviceHub from 'material-ui/svg-icons/hardware/device-hub';
import _ from 'lodash';

export default class NNCurrentStatus extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    const lastTrainingResult = this.props.lastTrainingResult;
    const startTime = lastTrainingResult != undefined ? lastTrainingResult.startTime : '';
    const endTime = lastTrainingResult != undefined ? lastTrainingResult.endTime : '';
    const trainingMatches = lastTrainingResult != undefined ? lastTrainingResult.trainingMatches : '';
    const testingMatches = lastTrainingResult != undefined ? lastTrainingResult.testingMatches : '';
    const trainingAccuracy = lastTrainingResult != undefined ? lastTrainingResult.trainingAccuracy : '';
    const testingAccuracy = lastTrainingResult != undefined ? lastTrainingResult.testingAccuracy : '';
    return (
      <Card style={{textAlign: 'left'}}>
        <CardHeader
          title="Neural Network Training"
          subtitle={"Latest Result: " + new Date(endTime)}
          avatar={<DeviceHub />}/>
        <CardText>
          <Table>
            <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
              <TableRow>
                <TableHeaderColumn></TableHeaderColumn>
                <TableHeaderColumn>Training</TableHeaderColumn>
                <TableHeaderColumn>Testing</TableHeaderColumn>
              </TableRow>
            </TableHeader>
            <TableBody displayRowCheckbox={false}>
                <TableRow>
                  <TableRowColumn>
                    Count
                  </TableRowColumn>
                  <TableRowColumn>
                    { trainingMatches } matches
                  </TableRowColumn>
                  <TableRowColumn>
                    { testingMatches } matches
                  </TableRowColumn>
                </TableRow>
                <TableRow>
                  <TableRowColumn>
                    Accuracy
                  </TableRowColumn>
                  <TableRowColumn>
                    <span> { _.round(trainingAccuracy, 2) }% </span>
                    <LinearProgress mode="determinate" value={ _.round(trainingAccuracy, 2) } />
                  </TableRowColumn>
                  <TableRowColumn>
                    <span> { _.round(testingAccuracy, 2) }% </span>
                    <LinearProgress mode="determinate" value={ _.round(testingAccuracy, 2) } />
                  </TableRowColumn>
                </TableRow>
            </TableBody>
          </Table>
        </CardText>
      </Card>
    );
  }
}

NNCurrentStatus.propTypes = {
  lastTrainingResult: React.PropTypes.object,
};
