import React from 'react';
import Paper from 'material-ui/Paper';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import appTheme from '../AppTheme.js';
import _ from 'lodash';

export default class ContentHolder extends React.Component {
  constructor(props){
    super(props);
  }

  render(){

    const style = {
      marginTop: 30,
      marginLeft: '5%',
      marginRight: '5%',
      display: 'inline-block',
      verticalAlign: 'top',
      width: '90%',
    };

    return (
      <MuiThemeProvider muiTheme={ appTheme }>
        <Paper style={ _.merge(style, this.props.style) } zDepth={4} >
          {this.props.children}
        </Paper>
      </MuiThemeProvider>
    );
  }
}
