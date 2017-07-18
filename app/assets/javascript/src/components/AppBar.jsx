import React from 'react';
import Bar from 'material-ui/AppBar';
import Popover from 'material-ui/Popover';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import appTheme from '../AppTheme.js';
import AppMenu from './AppMenu.jsx';

import IconButton from 'material-ui/IconButton';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';

export default class AppBar extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      open: false,
    };
    this.handleTouchTap = this.handleTouchTap.bind(this);
    this.handleRequestClose = this.handleRequestClose.bind(this);
  }

  handleTouchTap(event) {
    event.preventDefault();
    this.setState({
      open: true,
      anchorEl: event.currentTarget,
    });
  }

  handleRequestClose() {
    this.setState({
      open: false,
    });
  }

  loginInfo() {
    if (USER_AUTHENTICATED === "true"){
      return (
        <div className="user-info">
          <span>{USER_NAME}</span>
          <IconMenu
              iconButtonElement={
                <IconButton iconStyle={{color:'white', fontSize:"20px"}}><MoreVertIcon /></IconButton>
              }
              targetOrigin={{horizontal: 'right', vertical: 'top'}}
              anchorOrigin={{horizontal: 'right', vertical: 'bottom'}}
            >
            <MenuItem primaryText="Logout" href="/logout" />
          </IconMenu>
        </div>
      );
    }
    return (
      <a className="login-link" href={LOGIN_URL}>
        <img
          src="https://steamcommunity-a.akamaihd.net/public/images/signinthroughsteam/sits_01.png"/>
      </a>
    )
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={ appTheme } >
        <div>
          <Bar
            title="HOUSE o' DOTA"
            className='app-bar'
            onLeftIconButtonTouchTap={this.handleTouchTap} >
            {this.loginInfo()}
            <img className='logo' src='/static/images/logo_dota.png'/>
          </Bar>
          <Popover
            open={this.state.open}
            anchorEl={this.state.anchorEl}
            anchorOrigin={{horizontal: 'left', vertical: 'bottom'}}
            targetOrigin={{horizontal: 'left', vertical: 'top'}}
            onRequestClose={this.handleRequestClose}
            >
            <AppMenu />
          </Popover>
        </div>
      </MuiThemeProvider>
    );
  }
}
