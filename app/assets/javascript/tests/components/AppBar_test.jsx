import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import { expect } from 'chai';

import AppBar from  '../../src/components/AppBar.jsx';
import Popover from 'material-ui/Popover';
import AppMenu from  '../../src/components/AppMenu.jsx';

describe('<AppBar />', () => {
  it('renders two children', () => {
    const wrapper = shallow(<AppBar />);
    expect(wrapper.find(AppMenu)).to.have.length(1);
    expect(wrapper.find(Popover)).to.have.length(1);
  });

  it('renders closed popover', () => {
    const wrapper = shallow(<AppBar />);
    const popover = wrapper.find(Popover);
    expect(popover.props().open).to.be.false;
  });

  it('opens popover once menu button is clicked', () => {
    const wrapper = mount(<AppBar />);
    const node = ReactDOM.findDOMNode(
        ReactTestUtils.findRenderedDOMComponentWithTag(
          wrapper.instance(), 'button'
        )
      );
    ReactTestUtils.Simulate.touchTap(node);
    const popover = wrapper.find(Popover);
    expect(popover.props().open).to.be.true;
  });
});
