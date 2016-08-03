import React from 'react';
import Bar from 'material-ui/AppBar';
import Popover from 'material-ui/Popover';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import appTheme from '../AppTheme.js';
import AppMenu from './AppMenu.jsx';

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

  render() {
    return (
      <MuiThemeProvider muiTheme={ appTheme }>
        <div>
          <Bar
            title="HOUSE o' DOTA"
            className='app-bar'
            onLeftIconButtonTouchTap={this.handleTouchTap} >
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
