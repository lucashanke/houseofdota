import React from 'react';
import _ from 'lodash';

import { GridList, GridTile, IconButton } from 'material-ui';
import Add from 'material-ui/svg-icons/content/add';

const styles = {
  titleStyle: {
    color: '#fff',
    fontSize: '14px',
  },
  subtitleStyle: {
    color: '#fff',
    fontSize: '10px',
  },
  smallIcon: {
    width: 20,
    height: 20,
  },
  small: {
    width: 30,
    height: 30,
    padding: 5,
  },
  wrapper: {
    padding: '0.5%',
    textAlign: 'center',
    backgroundColor: 'rgb(232, 232, 232)',
  },
};

export default class RecommendedHeroes extends React.Component {

  render() {
    if (this.props.recommended.length === 0) {
      return (
        <div style={{ height: '70px' }}>
          <div className="spinning-wheel"/>
        </div>
      );
    }
    return(
      <div>
        <div style={styles.wrapper}>
          <GridList cols={5} cellHeight={120}>
            {this.props.recommended.map((hero) => (
              <GridTile
                key={hero.id}
                title={
                  <span style={styles.titleStyle} title={hero.name}>
                    {hero.name}
                  </span>
                }
                titleStyle={styles.titleStyle}
                subtitle={
                  !_.isNil(hero.bundleSize) ?
                  <span style={styles.subtitleStyle}>
                    {'based on'}<br/>
                    {`${hero.bundleSize-1} ally(ies)`}
                  </span> : !_.isNil(hero.counterFor) ?
                  <span style={styles.subtitleStyle}>
                    {'based on'}<br/>
                  {`${hero.counterFor} enemy(ies)`}
                  </span> : null
                }
                actionIcon={
                  <IconButton
                    iconStyle={styles.smallIcon}
                    style={styles.small}
                    className="pick-recommended-button"
                    onTouchTap={() => this.props.onPickAction(hero.id)}>
                    <Add color={styles.titleStyle.color}/>
                  </IconButton>
                }
                titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
              >
                <img src={'/static/images/' + (hero.id) + '.png'} />
              </GridTile>
            ))}
          </GridList>
        </div>
      </div>
    );
  }
}

RecommendedHeroes.propTypes = {
  recommended: React.PropTypes.array.isRequired,
  onPickAction: React.PropTypes.func.isRequired,
}
