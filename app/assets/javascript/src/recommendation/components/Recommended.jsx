import React from 'react';
import { Toolbar, ToolbarTitle } from 'material-ui';

import ContentHolder from '../../components/ContentHolder.jsx';
import RecommendedHeroes from './RecommendedHeroes.jsx';

const Recommended = (props) => {
  let recommendedAllies = null;
  if (props.recommendedAllies && !props.fullLineUp) {
    recommendedAllies = (
      <ContentHolder style={{width: '42.5%', marginRight: '2.5%'}}>
        <Toolbar>
          <ToolbarTitle text="Recommended based on Allies"/>
        </Toolbar>
        <RecommendedHeroes
          className="recommended-allies"
          recommended={props.recommendedAllies}
          onPickAction={props.onTapOfRecommended}
        />
      </ContentHolder>
    );
  }

  let recommendedCounters = null;
  if (props.recommendedCounters && !props.fullLineUp) {
    recommendedCounters = (
      <ContentHolder style={{width: '42.5%', marginLeft: '2.5%', float: 'right'}}>
        <Toolbar>
          <ToolbarTitle text="Recommended based on Enemies"/>
        </Toolbar>
        <RecommendedHeroes
          className="recommended-counters"
          recommended={props.recommendedCounters}
          onPickAction={props.onTapOfRecommended}
        />
      </ContentHolder>
    );
  }

  return (
    <div>
      {recommendedAllies}
      {recommendedCounters}
    </div>
  );
}

export default Recommended;
