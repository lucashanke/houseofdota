import React from 'react';
import ReactDOM from 'react-dom';

import injectTapEventPlugin from 'react-tap-event-plugin';
import AppBar from './components/AppBar.jsx';
import Statistics from './statistics/components/Statistics.jsx';

import '../../scss/index.scss';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

ReactDOM.render(<AppBar />, document.getElementById('app-bar'));
ReactDOM.render(<Statistics />, document.getElementById('statistics'));
