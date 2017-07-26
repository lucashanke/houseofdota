import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';
import sinon from 'sinon';

import LineUpSelection from  '../../../src/recommendation/components/LineUpSelection.jsx';

describe('<LineUpSelection />', () => {

  const onEnemySelectionSpy = sinon.spy();
  const onAllySelectionSpy = sinon.spy();

  const testDefaultProps = {
    availableHeroes: [
      { heroId: 1, localizedName: 'Anti-Mage' },
      { heroId: 2, localizedName: 'Axe' },
      { heroId: 3, localizedName: 'Perobinha' },
    ],
    disableAllySelection: false,
    disableEnemySelection: false,
    onEnemySelection: onEnemySelectionSpy,
    onAllySelection: onAllySelectionSpy,
  };

  it('renders two toolbar groups - one for allies and one for enemies', () => {
    const wrapper = shallow(<LineUpSelection {...testDefaultProps}/>);
    expect(wrapper.find('ToolbarGroup')).to.have.length(2);
  });

  it('renders two AutoComplete - one for allies and one for enemies', () => {
    const wrapper = shallow(<LineUpSelection {...testDefaultProps}/>);
    expect(wrapper.find('AutoComplete')).to.have.length(2);
  });

  it('sets AutoCompletes datasource corresponding to availableHeroes props', () => {
    const wrapper = shallow(<LineUpSelection {...testDefaultProps}/>);
    expect(wrapper.find('AutoComplete').first().props().dataSource).to.have.length(3);
  });


});
