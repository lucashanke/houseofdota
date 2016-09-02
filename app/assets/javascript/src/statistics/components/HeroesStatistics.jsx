import React from 'react';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';
import {Tabs, Tab} from 'material-ui/Tabs';
import LinearProgress from 'material-ui/LinearProgress';
import Star from 'material-ui/svg-icons/toggle/star';
import CheckBox from 'material-ui/svg-icons/toggle/check-box';
import _ from 'lodash';

import ContentHolder from '../../components/ContentHolder.jsx';


export default class HeroesStatistics extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      orderBy: 'pickRate',
    };
  }

  orderByPickRate(){
    this.setState({
      orderBy: 'pickRate',
    });
  }

  orderByWinRate(){
    this.setState({
      orderBy: 'pickRate',
    });
  }

  orderByConfidence(){
    this.setState({
      orderBy: 'confidence',
    });
  }

  render(){
    const statistics = _.orderBy(this.props.statistics, [this.state.orderBy], ['desc']);
    return(
      <ContentHolder>
        <Tabs>
          <Tab
            icon={<CheckBox />}
            label="MOST PICKED"
            onActive={ this.orderByPickRate.bind(this) }
            />
          <Tab
            icon={<Star />}
            label="MOST SUCCESSFUL"
            onActive={ this.orderByWinRate.bind(this) }
            />
          <Tab
            icon={<Star />}
            label="MOST CONFIDENT"
            onActive={ this.orderByConfidence.bind(this) }
            />
        </Tabs>
        <Table>
          <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
            <TableRow>
              <TableHeaderColumn colSpan={2} style={{width: '35%'}}>Hero</TableHeaderColumn>
              <TableHeaderColumn>Pick Rate</TableHeaderColumn>
              <TableHeaderColumn>Win Rate</TableHeaderColumn>
              <TableHeaderColumn>Confidence</TableHeaderColumn>
            </TableRow>
          </TableHeader>
          <TableBody displayRowCheckbox={false}>
            {statistics.map( (row) => (
              <TableRow key={row.heroId} >
                <TableRowColumn style={{width: '10%'}}>
                  <img src={'/static/images/' + row.heroId + '.png'} style={{height: '3em'}}/>
                </TableRowColumn>
                <TableRowColumn style={{width: '25%'}}>
                  { row.heroName }
                </TableRowColumn>
                <TableRowColumn>
                  { _.round(row.pickRate, 2) }
                  <LinearProgress mode="determinate" value={ _.round(row.pickRate, 2) } />
                </TableRowColumn>
                <TableRowColumn>
                  { _.round(row.winRate, 2) }
                  <LinearProgress mode="determinate" value={ _.round(row.winRate, 2) } />
                </TableRowColumn>
                <TableRowColumn>
                  { _.round(row.confidence, 2) }
                  <LinearProgress mode="determinate" value={ _.round(row.confidence, 2) } />
                </TableRowColumn>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </ContentHolder>
    );
  }
}

HeroesStatistics.propTypes = {
  matchQuantity: React.PropTypes.number.isRequired,
  statistics: React.PropTypes.array.isRequired,
};
