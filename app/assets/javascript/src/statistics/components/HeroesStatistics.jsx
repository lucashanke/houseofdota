import React from 'react';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';
import LinearProgress from 'material-ui/LinearProgress';
import _ from 'lodash';

import ContentHolder from '../../components/ContentHolder.jsx';

const HeroesStatistics = (props) => {
  const statistics = _.orderBy( props.statistics ,[props.orderBy], ['desc']);
  return(
    <ContentHolder>
      <Table>
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
          <TableRow>
            <TableHeaderColumn style={{ textAlign: 'center', width: "40%" }}>Heroes</TableHeaderColumn>
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
          { statistics.map( (row) => (
            <TableRow key={row.id}  >
              <TableRowColumn style={{ textAlign: 'center', width: "40%" }}>
              { row.heroBundle.map( (hero) => (
                <div style={ { float: "left" } } key={ row.id + hero.id }>
                  <img src={'/static/images/' + hero.id + '.png'} style={{height: '3em', marginRight: '1em'}}/>
                </div>
              ))}
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
