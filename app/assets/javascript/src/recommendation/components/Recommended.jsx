import React from 'react';
import { GridList, GridTile, IconButton } from 'material-ui';
import Add from 'material-ui/svg-icons/content/add';

const styles = {
  titleStyle: {
    color: '#fff',
  },
};

export default class Recommended extends React.Component {

  getUndefinedHeroesTiles(quantity) {
    const tiles = [];
    for(let i = 0; i < quantity; i++){
      tiles.push((
        <GridTile
          title={'Undefined'}
          titleStyle={styles.titleStyle}
          titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
        >
          <img src={'/static/images/0.png'} />
        </GridTile>
      ));
    }
    return tiles;
  }

  render() {
    return(
      <div>
        <div style={{ width: '99%', display: 'inline-block', padding: '0.5%'}}>
          <GridList cols={5} cellHeight={120}>
            {this.props.recommended.map((hero) => (
              <GridTile
                key={hero.id}
                title={hero.name}
                titleStyle={styles.titleStyle}
                actionIcon={
                  <IconButton onTouchTap={() => this.props.onPickAction(hero.id)}>
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
