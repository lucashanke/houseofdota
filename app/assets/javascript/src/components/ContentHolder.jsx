import React from 'react';
import Paper from 'material-ui/Paper';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import appTheme from '../AppTheme.js';


export default class ContentHolder extends React.Component {
  constructor(props){
    super(props);
  }

  render(){

    const style = {
      marginTop: 30,
      marginLeft: 70,
      marginRight: 70,
      marginBottom: 30,
      textAlign: 'center',
      display: 'inline-block',
    };

    return (
      <MuiThemeProvider muiTheme={ appTheme } >
        <Paper style={ style } zDepth={2} >
          {this.props.children}
        </Paper>
      </MuiThemeProvider>
    );
  }
}
