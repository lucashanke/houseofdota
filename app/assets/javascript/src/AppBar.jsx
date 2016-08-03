import React from 'react';
import Bar from 'material-ui/AppBar';
import Popover from 'material-ui/Popover';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

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
      <MuiThemeProvider>
        <div>
          <Bar
            title="House of DOTA"
            onLeftIconButtonTouchTap={this.handleTouchTap}
            />
          <Popover
            open={this.state.open}
            anchorEl={this.state.anchorEl}
            anchorOrigin={{horizontal: 'left', vertical: 'bottom'}}
            targetOrigin={{horizontal: 'left', vertical: 'top'}}
            onRequestClose={this.handleRequestClose}
            >
            <Menu>
              <MenuItem primaryText="Statistics" />
              <MenuItem primaryText="Recommendation" />
            </Menu>
          </Popover>
        </div>
      </MuiThemeProvider>
    );
  }
}
