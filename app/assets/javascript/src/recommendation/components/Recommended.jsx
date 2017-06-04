import React from 'react';
import { GridList, GridTile, IconButton } from 'material-ui';
import Add from 'material-ui/svg-icons/content/add';

const styles = {
  titleStyle: {
    color: '#fff',
    fontSize: '14px',
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
    display: 'inline-block',
    padding: '0.5%',
    textAlign: 'center',
  }
};

export default class Recommended extends React.Component {

  getUndefinedHeroesTiles(quantity) {
    const tiles = [];
    for(let i = 0; i < quantity; i++){
      tiles.push((
        <GridTile
          title={''}
          titleStyle={styles.titleStyle}
          titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
        >
          <img src={'/static/images/logo_dota.png'} />
        </GridTile>
      ));
    }
    return tiles;
  }

  render() {
    return(
      <div>
        <div style={styles.wrapper}>
          <GridList cols={5} cellHeight={120}>
            {this.props.recommended.map((hero) => (
              <GridTile
                key={hero.id}
                style={{ borderRadius: '16px' }}
                title={
                  <span style={styles.titleStyle} title={hero.name}>
                    {hero.name}
                  </span>
                }
                titleStyle={styles.titleStyle}
                actionIcon={
                  <IconButton
                    iconStyle={styles.smallIcon}
                    style={styles.small}
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

Recommended.propTypes = {
  recommended: React.PropTypes.array.isRequired,
  onPickAction: React.PropTypes.func.isRequired,
}
