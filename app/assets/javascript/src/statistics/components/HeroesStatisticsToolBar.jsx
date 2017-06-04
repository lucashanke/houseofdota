import React, { Component, PropTypes} from 'react';
import { Toolbar, ToolbarGroup, ToolbarTitle,
  ToolbarSeparator, DropDownMenu, FontIcon, MenuItem } from 'material-ui';
import SortIcon from 'material-ui/svg-icons/content/sort';
import ContentHolder from '../../components/ContentHolder.jsx';

const HeroesStatisticsToolBar = (props) => {
  return (
    <ContentHolder style={{ marginTop: 0 }}>
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
          </DropDownMenu>
        <ToolbarSeparator />
          <FontIcon className="material-icons">group_work</FontIcon>
          <DropDownMenu value={ props.bundleSize } onChange={ props.onBundleSizeChange }>
            <MenuItem value={ 1 } label="Bundle size: 1 hero" primaryText="1 hero" />
            <MenuItem value={ 2 } label="Bundle size: 2 heroes" primaryText="2 heroes" />
            <MenuItem value={ 3 } label="Bundle size: 3 heroes" primaryText="3 heroes" />
            <MenuItem value={ 4 } label="Bundle size: 4 heroes" primaryText="4 heroes" />
            <MenuItem value={ 5 } label="Bundle size: 5 heroes" primaryText="5 heroes" />
          </DropDownMenu>
        </ToolbarGroup>
      </Toolbar>
    </ContentHolder>
  );
}

HeroesStatisticsToolBar.propTypes = {
  orderBy: PropTypes.string.isRequired,
  bundleSize: PropTypes.number.isRequired,
  matchQuantity: PropTypes.number.isRequired,
  onOrderChange: PropTypes.func.isRequired,
  onBundleSizeChange: PropTypes.func.isRequired,
}

export default HeroesStatisticsToolBar;
