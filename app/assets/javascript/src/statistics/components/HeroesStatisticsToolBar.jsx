import React, { Component, PropTypes} from 'react';
import { Toolbar, ToolbarGroup, ToolbarTitle,
  ToolbarSeparator, DropDownMenu, FontIcon, MenuItem } from 'material-ui';
import SortIcon from 'material-ui/svg-icons/content/sort';


const HeroesStatisticsToolBar = (props) => {
  return (
    <Toolbar>
      <ToolbarGroup firstChild={false}>
        <ToolbarTitle text= { "Matches Collected: " + props.matchQuantity } />
      </ToolbarGroup>
      <ToolbarGroup>
        <ToolbarSeparator />
        <FontIcon className="material-icons">sort</FontIcon>
        <DropDownMenu value={ props.orderBy } onChange={ props.onOrderChange } >
          <MenuItem value={'pickRate'} label="Sort by: Pick Rate" primaryText="Pick Rate" />
          <MenuItem value={'winRate'} label="Sort by: Win Rate" primaryText="Win Rate" />
          <MenuItem value={'confidence'} label="Sort by: Confidence" primaryText="Confidence" />
        </DropDownMenu>
      <ToolbarSeparator />
        <FontIcon className="material-icons">group_work</FontIcon>
        <DropDownMenu value={ 1 }>
          <MenuItem value={ 1 } label="Bundle size: 1 hero" primaryText="1 hero" />
        </DropDownMenu>
      </ToolbarGroup>
    </Toolbar>
  );
}

HeroesStatisticsToolBar.propTypes = {
  orderBy: PropTypes.string.isRequired,
  matchQuantity: PropTypes.number.isRequired,
  onOrderChange: PropTypes.func.isRequired,
}

export default HeroesStatisticsToolBar;
