import React from 'react';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import Home from 'material-ui/svg-icons/action/home';
import TrendingUp from 'material-ui/svg-icons/action/trending-up';
import ThumbsUpDown from 'material-ui/svg-icons/action/thumbs-up-down';
import DeviceHub from 'material-ui/svg-icons/hardware/device-hub';

export default class AppMenu extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    return (
      <Menu>
        <MenuItem
          linkButton={true}
          href="/"
          primaryText="Home"
          leftIcon={<Home />}/>
        <MenuItem
          linkButton={true}
          href="/statistics"
          primaryText="Statistics"
          leftIcon={<TrendingUp />}/>
        <MenuItem
          linkButton={true}
          href="/recommendation"
          primaryText="Recommendation"
          leftIcon={<ThumbsUpDown />} />
        <MenuItem
          linkButton={true}
          href="/nn_performance"
          primaryText="NN Performance"
          leftIcon={<DeviceHub />} />
      </Menu>
    );
  }
}
