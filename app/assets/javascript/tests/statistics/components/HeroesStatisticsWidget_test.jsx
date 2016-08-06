import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';
import sinon from  'sinon';

import HeroesStatisticsWidget from '../../../src/statistics/components/HeroesStatisticsWidget.jsx';
import HeroesStatistics from '../../../src/statistics/components/HeroesStatistics.jsx';

describe('<HeroesStatisticsWidget />', () => {

  let getJSON;

  beforeEach(() => {
    getJSON = sinon.stub($, 'getJSON');
  });

  afterEach(() => {
    $.getJSON.restore();
  });

  it('renders a HeroesStatistics component as child', () => {
    getJSON.yields('/statistics/heroes', {});
    const wrapper = shallow(<HeroesStatisticsWidget />);
    expect(wrapper.find(HeroesStatistics)).to.have.length(1);
  });

});
