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
            <TableHeaderColumn sstyle={{
                textAlign: 'center',
                fontWeight: props.orderBy === 'pickRate' ? 'bold' : 'normal',
              }}>
              Pick Rate
            </TableHeaderColumn>
            <TableHeaderColumn style={{
                textAlign: 'center',
                fontWeight: props.orderBy === 'winRate' ? 'bold' : 'normal',
              }}>
              Win Rate
            </TableHeaderColumn>
          </TableRow>
        </TableHeader>
        <TableBody displayRowCheckbox={false} showRowHover={true}>
          { statistics.map( (row) => (
            <TableRow key={row.id}  >
              <TableRowColumn style={{ textAlign: 'center', width: "40%" }}>
              { row.heroes.map( (hero) => (
                <div style={ { float: "left" } } key={ row.id + hero.id }>
                  <img
                    src={'/static/images/' + hero.id + '.png'}
                    title={hero.name}
                    style={{height: '3em', marginRight: '0.5em'}}
                  />
                </div>
              ))}
              </TableRowColumn>
              <TableRowColumn>
                { _.round(row.pickRate*100, 2) }%
                <LinearProgress
                  color={ props.orderBy == 'pickRate' ? 'rgb(183, 28, 28)' : ''  }
                  mode="determinate"
                  value={ _.round(row.pickRate*100, 2) }
                />
              </TableRowColumn>
              <TableRowColumn>
                { _.round(row.winRate*100, 2) }%
                <LinearProgress
                  color={ props.orderBy == 'winRate' ? 'rgb(183, 28, 28)' : ''  }
                  mode="determinate"
                  value={ _.round(row.winRate*100, 2) } />
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
