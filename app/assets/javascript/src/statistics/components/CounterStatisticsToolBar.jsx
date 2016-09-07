import React, { Component, PropTypes} from 'react';
import { Toolbar, ToolbarGroup, ToolbarTitle,
  ToolbarSeparator, DropDownMenu, FontIcon, MenuItem, AutoComplete } from 'material-ui';
import ContentHolder from '../../components/ContentHolder.jsx';

const CounterStatisticsToolBar = (props) => {
  const heroes = CounterStatisticsToolBar.constructHeroesOptions(props.heroes);
  return (
    <ContentHolder style={{ marginTop: 0  }}>
      <Toolbar>
        <ToolbarGroup firstChild={false}>
          <ToolbarTitle text= { "Matches Collected: " + props.matchQuantity } />
        </ToolbarGroup>
        <ToolbarGroup>
          <ToolbarSeparator />
          <FontIcon className="material-icons"
            style={{ marginRight: '0.5em' }}>person_pin</FontIcon>
          <AutoComplete
            filter={AutoComplete.fuzzyFilter}
            openOnFocus={true}
            dataSource={ heroes }
            hintText="Select your Hero"
            onNewRequest={ props.onHeroChange }/>
          <ToolbarSeparator />
          <FontIcon className="material-icons">sort</FontIcon>
          <DropDownMenu value={ props.orderBy } onChange={ props.onOrderChange } >
            <MenuItem value={'counterCoefficient'} label="Sort by: Counter Coefficient" primaryText="Counter Coefficient" />
            <MenuItem value={'rateAdvantageNormalized'} label="Sort by: Rate Advantage" primaryText="Rate Advantage" />
          </DropDownMenu>
        </ToolbarGroup>
      </Toolbar>
    </ContentHolder>
  );
}

CounterStatisticsToolBar.propTypes = {
  orderBy: PropTypes.string.isRequired,
  heroId: PropTypes.number,
  matchQuantity: PropTypes.number.isRequired,
  onOrderChange: PropTypes.func.isRequired,
  onHeroChange: PropTypes.func.isRequired,
}

CounterStatisticsToolBar.constructHeroesOptions = (heroes) => {
  if (heroes !== undefined) return heroes.map( (hero) => {
    return {
      valueKey: hero.heroId,
      text: hero.localizedName,
      value: (
        <MenuItem
          primaryText={ hero.localizedName } >
        </MenuItem>
      ),
    };
  });
  return [];
}

export default CounterStatisticsToolBar;
