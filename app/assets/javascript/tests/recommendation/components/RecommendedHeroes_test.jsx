import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';
import sinon from 'sinon';

import RecommendedHeroes from  '../../../src/recommendation/components/RecommendedHeroes.jsx';

describe('<RecommendedHeroes />', () => {

  const onPickActionSpy = sinon.spy();

  const testDefaultProps = {
    recommended: [
      { id: 6, localizedName: 'Drow' },
      { id: 7, localizedName: 'Earthshaker' },
      { id: 8, localizedName: 'Juggernaut' },
      { id: 9, localizedName: 'Mirana' },
      { id: 10, localizedName: 'Morphling' },
    ],
    onPickAction: onPickActionSpy,
  };

  it('renders one GridList for the recommended', () => {
    const wrapper = shallow(<RecommendedHeroes {...testDefaultProps}/>);
    expect(wrapper.find('GridList')).to.have.length(1);
  });

  it('renders GridTiles for each of the 5 recommended heroes', () => {
    const wrapper = shallow(<RecommendedHeroes {...testDefaultProps}/>);
    expect(wrapper.find('GridTile')).to.have.length(5);
  });

  it('calls onPickAction with hero id of the corresponding GridTile tapped', () => {
    const wrapper = shallow(<RecommendedHeroes {...testDefaultProps}/>);
    const actionIcon = wrapper.find('GridTile').get(0).props.actionIcon;
    expect(actionIcon).to.not.be.null;
    actionIcon.props.onTouchTap();
    expect(onPickActionSpy.calledWith(6)).to.be.true;
  });

  afterEach(() => {
    onPickActionSpy.reset();
  });

});
