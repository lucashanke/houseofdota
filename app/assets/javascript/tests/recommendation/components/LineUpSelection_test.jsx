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
    expect(wrapper.find('AutoComplete').get(0).props.dataSource).to.have.length(3);
    expect(wrapper.find('AutoComplete').get(1).props.dataSource).to.have.length(3);
  });

  it('disables allies\' AutoComplete if disableAllySelection is true', () => {
    const wrapper = shallow(<LineUpSelection {...testDefaultProps} disableAllySelection/>);
    expect(wrapper.find('AutoComplete').get(0).props.disabled).to.be.eql(true);
  });

  it('disables enemies\' AutoComplete if disableEnemySelection is true', () => {
    const wrapper = shallow(<LineUpSelection {...testDefaultProps} disableEnemySelection/>);
    expect(wrapper.find('AutoComplete').get(1).props.disabled).to.be.eql(true);
  });

  it('calls onAllySelection prop when hero is selected', () => {
    const wrapper = shallow(<LineUpSelection {...testDefaultProps}/>);
    wrapper.find('AutoComplete').get(0).props.onNewRequest({valueKey: 1}, 0);
    expect(onAllySelectionSpy.calledWith(1)).to.be.eql(true)
  });

  it('calls onEnemySelection prop when hero is selected', () => {
    const wrapper = shallow(<LineUpSelection {...testDefaultProps}/>);
    wrapper.find('AutoComplete').get(1).props.onNewRequest({valueKey: 2}, 0);
    expect(onEnemySelectionSpy.calledWith(2)).to.be.eql(true)
  });

});
