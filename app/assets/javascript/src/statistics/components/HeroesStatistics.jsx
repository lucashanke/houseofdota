import React from 'react';

export default class HeroesStatistics extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    return(
      <div>
        Heroes Statistics
      </div>
    );
  }
}

HeroesStatistics.propTypes = {
  matchQuantity: React.PropTypes.number.isRequired,
  statistics: React.PropTypes.array.isRequired,
};
