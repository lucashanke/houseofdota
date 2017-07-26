import React from 'react';
import _ from 'lodash';

import { Toolbar,
  ToolbarGroup,
  ToolbarTitle,
  ToolbarSeparator,
  FontIcon,
  MenuItem,
  AutoComplete } from 'material-ui';

const initialState = {
  searchAlly: '',
  searchEnemy: '',
}

export default class LineUpSelection extends React.Component {

  constructor(props) {
    super(props);
    this.state = initialState;
  }

  constructHeroesOptions() {
    if (this.props.availableHeroes !== undefined) {
      return _.sortBy(this.props.availableHeroes, ['localizedName']).map(hero => {
        return {
          valueKey: hero.heroId,
          text: hero.localizedName,
          value: (
            <MenuItem
              primaryText={hero.localizedName}
            />
          ),
        };
      });
    }
    return [];
  }

  handleUpdateInputAlly(searchText) {
    this.setState({
      searchAlly: searchText,
    });
  };

  handleUpdateInputEnemy(searchText) {
    this.setState({
      searchEnemy: searchText,
    });
  };

  render() {
    return (
      <Toolbar>
        <ToolbarGroup>
          <FontIcon className="material-icons"
            style={{ marginRight: '0.5em' }}>person_pin</FontIcon>
          <AutoComplete
            ref={(c)=>{ this.allySelection = c; }}
            filter={AutoComplete.fuzzyFilter}
            openOnFocus={true}
            dataSource={this.constructHeroesOptions()}
            hintText="Select an Ally"
            searchText={this.state.searchAlly}
            disabled={this.props.disableAllySelection}
            onUpdateInput={this.handleUpdateInputAlly.bind(this)}
            onNewRequest={this.props.onAllySelection}
            menuProps={{desktop: true, maxHeight: 200}}/>
          <ToolbarSeparator />
        </ToolbarGroup>
        <ToolbarTitle text="Line-Up Selection"/>
        <ToolbarGroup>
          <ToolbarSeparator />
          <FontIcon className="material-icons"
            style={{ marginRight: '0.5em' }}>person_pin</FontIcon>
          <AutoComplete
            ref={(c)=>{ this.enemySelection = c; }}
            filter={AutoComplete.fuzzyFilter}
            openOnFocus={true}
            dataSource={this.constructHeroesOptions()}
            hintText="Select an Enemy"
            searchText={this.state.searchEnemy}
            disabled={this.props.disableEnemySelection}
            onUpdateInput={this.handleUpdateInputEnemy.bind(this)}
            onNewRequest={this.props.onEnemySelection}
            menuProps={{desktop: true, maxHeight: 200}}/>
        </ToolbarGroup>
      </Toolbar>
    );
  }

}

LineUpSelection.propTypes = {
  availableHeroes: React.PropTypes.arrayOf(React.PropTypes.shape({
    localizedName: React.PropTypes.string.isRequired,
    heroId: React.PropTypes.number.isRequired,
  })),
  disableEnemySelection: React.PropTypes.bool.isRequired,
  disableAllySelection: React.PropTypes.bool.isRequired,
  onEnemySelection: React.PropTypes.func.isRequired,
  onAllySelection: React.PropTypes.func.isRequired,
}
