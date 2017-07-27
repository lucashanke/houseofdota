import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';
import sinon from 'sinon';

import Recommended from  '../../../src/recommendation/components/Recommended.jsx';

describe('<Recommended />', () => {

  const onTapOfRecommendedSpy = sinon.spy();

  const testDefaultProps = {
    recommendedAllies: [
      { heroId: 1, localizedName: 'Anti-Mage' },
      { heroId: 2, localizedName: 'Axe' },
      { heroId: 3, localizedName: 'Bane' },
      { heroId: 4, localizedName: 'Bloodseeker' },
      { heroId: 5, localizedName: 'Crystal' },
    ],
    recommendedCounters: [
      { heroId: 6, localizedName: 'Drow' },
      { heroId: 7, localizedName: 'Earthshaker' },
      { heroId: 8, localizedName: 'Juggernaut' },
      { heroId: 9, localizedName: 'Mirana' },
      { heroId: 10, localizedName: 'Morphling' },
    ],
    fullLineUp: false,
    onTapOfRecommended: onTapOfRecommendedSpy,
  };

  it('doesnt render RecommendedHeroes for allies if recommendedAllies are undefined', () => {
    const wrapper = shallow(<Recommended {...testDefaultProps} recommendedAllies={null}/>);
    expect(wrapper.find('RecommendedHeroes.recommended-allies')).to.have.length(0);
  });

  it('renders RecommendedHeroes for allies if recommendedAllies are defined', () => {
    const wrapper = shallow(<Recommended {...testDefaultProps}/>);
    expect(wrapper.find('RecommendedHeroes.recommended-allies')).to.have.length(1);
  });

  it('doesnt render RecommendedHeroes for counters if recommendedCounters are undefined', () => {
    const wrapper = shallow(<Recommended {...testDefaultProps} recommendedCounters={null}/>);
    expect(wrapper.find('RecommendedHeroes.recommended-counters')).to.have.length(0);
  });

  it('renders RecommendedHeroes for counters if recommendedCounters are defined', () => {
    const wrapper = shallow(<Recommended {...testDefaultProps}/>);
    expect(wrapper.find('RecommendedHeroes.recommended-counters')).to.have.length(1);
  });

  it('doesnt render any RecommendedHeroes if line-up is full', () => {
    const wrapper = shallow(<Recommended {...testDefaultProps} fullLineUp={true}/>);
    expect(wrapper.find('RecommendedHeroes')).to.have.length(0);
  });

  it('pass onTapOfRecommended to RecommendedHeroes onPickAction prop', () => {
    const wrapper = shallow(<Recommended {...testDefaultProps}/>);
    expect(wrapper.find('RecommendedHeroes').get(0).props.onPickAction).to.be.eql(onTapOfRecommendedSpy);
    expect(wrapper.find('RecommendedHeroes').get(1).props.onPickAction).to.be.eql(onTapOfRecommendedSpy);
  });

  afterEach(() => {
    onTapOfRecommendedSpy.reset();
  });

});
