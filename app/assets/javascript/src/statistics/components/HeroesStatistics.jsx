import React from 'react';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';
import LinearProgress from 'material-ui/LinearProgress';
import _ from 'lodash';

import ContentHolder from '../../components/ContentHolder.jsx';

const HeroesStatistics = (props) => {
  const statistics = _.orderBy([props.statistics, props.orderBy], ['desc']);
  return(
    <ContentHolder>
      <Table>
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
          <TableRow>
            <TableHeaderColumn colSpan={2} style={{width: '35%'}}>Hero</TableHeaderColumn>
            <TableHeaderColumn style={{ textAlign: 'center' }}>
              Pick Rate
            </TableHeaderColumn>
            <TableHeaderColumn style={{ textAlign: 'center' }}>
              Win Rate
            </TableHeaderColumn>
            <TableHeaderColumn style={{ textAlign: 'center' }}>
              Confidence
            </TableHeaderColumn>
          </TableRow>
        </TableHeader>
        <TableBody displayRowCheckbox={false} showRowHover={true}>
          { props.statistics.map( (row) => (
            <TableRow key={row.heroId} >
              <TableRowColumn style={{width: '10%'}}>
                <img src={'/static/images/' + row.heroId + '.png'} style={{height: '3em'}}/>
              </TableRowColumn>
              <TableRowColumn style={{width: '25%'}}>
                { row.heroName }
              </TableRowColumn>
              <TableRowColumn>
                { _.round(row.pickRate, 2) }%
                <LinearProgress
                  color={ props.orderBy == 'pickRate' ? 'rgb(183, 28, 28)' : ''  }
                  mode="determinate"
                  value={ _.round(row.pickRate, 2) }
                />
              </TableRowColumn>
              <TableRowColumn>
                { _.round(row.winRate, 2) }%
                <LinearProgress
                  color={ props.orderBy == 'winRate' ? 'rgb(183, 28, 28)' : ''  }
                  mode="determinate"
                  value={ _.round(row.winRate, 2) } />
              </TableRowColumn>
              <TableRowColumn>
                { _.round(row.confidence, 2) }%
                <LinearProgress
                  color={ props.orderBy == 'confidence' ? 'rgb(183, 28, 28)' : ''  }
                  mode="determinate" value={ _.round(row.confidence, 2) } />
              </TableRowColumn>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </ContentHolder>
  );
}

HeroesStatistics.propTypes = {
  statistics: React.PropTypes.array.isRequired,
  orderBy: React.PropTypes.string.isRequired,
};

export default HeroesStatistics;
