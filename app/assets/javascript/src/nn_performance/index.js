import React from 'react';
import ReactDOM from 'react-dom';

import injectTapEventPlugin from 'react-tap-event-plugin';
import NNPerformance from './components/NNPerformance.jsx';

import '../../../scss/index.scss';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

ReactDOM.render(<NNPerformance />, document.getElementById('nn-performance'));
