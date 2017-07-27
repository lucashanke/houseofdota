import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';
import sinon from 'sinon';

import Recommendation from  '../../../src/recommendation/components/Recommendation.jsx';

describe('<Recommendation />', () => {

  it('renders the LineUpSelection and LineUp inside a ContentHolder', () => {
    const wrapper = shallow(<Recommendation />);
    expect(wrapper.find('ContentHolder LineUpSelection')).to.have.length(1);
    expect(wrapper.find('ContentHolder LineUp')).to.have.length(1);
  });

});
