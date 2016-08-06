import React from 'react';
import { shallow } from 'enzyme';
import { expect } from 'chai';

import AppMenu from  '../../src/components/AppMenu.jsx';
import MenuItem from 'material-ui/MenuItem';

describe('<AppMenu />', () => {

  it('renders two items', () => {
    const wrapper = shallow(<AppMenu />);
    expect(wrapper.find(MenuItem)).to.have.length(2);
  });

  it('buttons have correct links', () => {
    const wrapper = shallow(<AppMenu />);
    const buttons = wrapper.find(MenuItem);
    expect(buttons.at(0).props().href).to.equal('/statistics');
  });

});
