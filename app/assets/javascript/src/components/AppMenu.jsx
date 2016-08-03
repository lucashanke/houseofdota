import React from 'react';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';

export default class AppMenu extends React.Component {

  constructor(props){
    super(props);
  }

  render(){
    return (
      <Menu>
        <MenuItem primaryText="Statistics" />
        <MenuItem primaryText="Recommendation" />
      </Menu>
    );
  }
}
