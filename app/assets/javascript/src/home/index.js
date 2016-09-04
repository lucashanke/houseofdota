import React from 'react';
import ReactDOM from 'react-dom';

import injectTapEventPlugin from 'react-tap-event-plugin';
import Home from './components/Home.jsx';

import '../../../scss/index.scss';
import '../../../scss/home.scss';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

ReactDOM.render(<Home />, document.getElementById('home'));
