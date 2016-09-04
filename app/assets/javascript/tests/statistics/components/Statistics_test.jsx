import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';

import Statistics from  '../../../src/statistics/components/Statistics.jsx';
import HeroesStatisticsWidget from  '../../../src/statistics/components/HeroesStatisticsWidget.jsx';
import ContentHolder from  '../../../src/components/ContentHolder.jsx';

describe('<Statistics />', () => {

  it('renders a ContentHolder with a HeroesStatisticsWidget as child', () => {
    const wrapper = shallow(<Statistics />);
    expect(wrapper.find(HeroesStatisticsWidget)).to.have.length(1);
  });

});
