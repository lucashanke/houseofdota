import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';
import sinon from 'sinon';

import LineUp from  '../../../src/recommendation/components/LineUp.jsx';

describe('<LineUp />', () => {

  const onActionSpy = sinon.spy();

  const testDefaultProps = {
    allies: [
      { heroId: 1, localizedName: 'Anti-Mage' },
      { heroId: 3, localizedName: 'Perobinha' },
    ],
    enemies: [
      { heroId: 2, localizedName: 'Axe' },
    ],
    onAction: onActionSpy,
  };

  it('renders two GridLists - one for allies and one for enemies', () => {
    const wrapper = shallow(<LineUp {...testDefaultProps}/>);
    expect(wrapper.find('GridList')).to.have.length(2);
  });

  it('renders GridTiles for each of the 10 slots', () => {
    const wrapper = shallow(<LineUp {...testDefaultProps}/>);
    expect(wrapper.find('GridTile')).to.have.length(10);
  });

  it('renders 5 GridTiles for each team', () => {
    const wrapper = shallow(<LineUp {...testDefaultProps}/>);
    expect(wrapper.find('GridList.allies-grid GridTile')).to.have.length(5);
    expect(wrapper.find('GridList.enemies-grid GridTile')).to.have.length(5);
  });

  it('renders GridTiles for the heroes still to be defined', () => {
    const wrapper = shallow(<LineUp {...testDefaultProps}/>);
    expect(wrapper.find('GridList.allies-grid GridTile.tile-undefined')).to.have.length(3);
    expect(wrapper.find('GridList.enemies-grid GridTile.tile-undefined')).to.have.length(4);
  });

  it('renders first GridTiles for selected allies with proper action passed', () => {
    const wrapper = shallow(<LineUp {...testDefaultProps}/>);
    const actionIcon = wrapper.find('GridList.allies-grid GridTile').get(0).props.actionIcon;
    expect(actionIcon).to.not.be.null;
    actionIcon.props.onTouchTap();
    expect(onActionSpy.calledWith(1)).to.be.true;
  });

  it('renders last GridTiles for selected enemies with proper action passed', () => {
    const wrapper = shallow(<LineUp {...testDefaultProps}/>);
    const actionIcon = wrapper.find('GridList.enemies-grid GridTile').get(4).props.actionIcon;
    expect(actionIcon).to.not.be.null;
    actionIcon.props.onTouchTap();
    expect(onActionSpy.calledWith(2)).to.be.true;
  });

  afterEach(() => {
    onActionSpy.reset();
  });

});
