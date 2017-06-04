import React from 'react';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';
import LinearProgress from 'material-ui/LinearProgress';
import _ from 'lodash';

import ContentHolder from '../../components/ContentHolder.jsx';

const CounterStatistics = (props) => {
  const counters = _.orderBy( props.counters ,[props.orderBy], ['desc']);
  const maxCoeffient = _.maxBy( counters , 'counterCoefficient');
  const minCoeffient = _.minBy( counters , 'counterCoefficient');
  return(
    <ContentHolder>
      <Table>
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
          <TableRow>
            <TableHeaderColumn style={{ textAlign: 'center', width: "20%" }}>Heroes</TableHeaderColumn>
            <TableHeaderColumn style={{ textAlign: 'center', width: "20%" }}></TableHeaderColumn>
            <TableHeaderColumn style={{ textAlign: 'center' }}>
              Counter Coefficient
            </TableHeaderColumn>
            <TableHeaderColumn style={{ textAlign: 'center' }}>
              Relation Dependency
            </TableHeaderColumn>
          </TableRow>
        </TableHeader>
        <TableBody displayRowCheckbox={false} showRowHover={true}>
          { counters.map( (row) => (
            <TableRow key={row.id}  >
              <TableRowColumn style={{ textAlign: 'center', width: "20%"}}>
                  <img src={'/static/images/' + row.id + '.png'} style={{height: '3em', marginRight: '1em'}}/>
              </TableRowColumn>
              <TableRowColumn style={{ width: "20%" }}>
                { row.name }
              </TableRowColumn>
              <TableRowColumn>
                { _.round(row.counterCoefficient, 2) }
                <LinearProgress
                  color={ props.orderBy == 'counterCoefficient' ? 'rgb(183, 28, 28)' : ''  }
                  mode="determinate"
                  value={ _.round(row.counterCoefficient, 2) }
                  max={ maxCoeffient.counterCoefficient }
                  min={ minCoeffient.counterCoefficient }
                />
              </TableRowColumn>
              <TableRowColumn>
                { _.round(row.lift , 2) }
                <LinearProgress
                  color={ props.orderBy == 'lift' ? 'rgb(183, 28, 28)' : ''  }
                  mode="determinate"
                  value={ _.round(row.lift, 2) }
                  min={0}
                  max={10}
                />
              </TableRowColumn>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </ContentHolder>
  );
}

CounterStatistics.propTypes = {
  counters: React.PropTypes.array.isRequired,
  orderBy: React.PropTypes.string.isRequired,
};

export default CounterStatistics;
