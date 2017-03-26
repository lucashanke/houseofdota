import React from 'react';
import { GridList, GridTile, IconButton } from 'material-ui';
import Clear from 'material-ui/svg-icons/content/clear';

const styles = {
  titleStyle: {
    color: '#fff',
  },
};

export default class LineUp extends React.Component {

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
        <div style={{ width: '49%', display: 'inline-block', padding: '0.5%'}}>
          <GridList cols={5} cellHeight={120}>
            {this.props.allies.map((ally) => (
              <GridTile
                key={ally.heroId}
                title={ally.localizedName}
                titleStyle={styles.titleStyle}
                titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
                actionIcon={
                  <IconButton onTouchTap={() => this.props.onAction(ally.heroId)}>
                    <Clear color={styles.titleStyle.color}/>
                  </IconButton>
                }
              >
                <img src={'/static/images/' + ally.heroId + '.png'} />
              </GridTile>
            ))}
            {this.getUndefinedHeroesTiles(5-this.props.allies.length)}
          </GridList>
        </div>

        <div style={{ width: '49%', display: 'inline-block', padding: '0.5%' }}>
          <GridList style={styles.gridList} cols={5} cellHeight={120}>
            {this.getUndefinedHeroesTiles(5-this.props.enemies.length)}
            {this.props.enemies.map((enemy) => (
              <GridTile
                key={enemy.heroId}
                title={enemy.localizedName}
                titleStyle={styles.titleStyle}
                titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
                actionIcon={
                  <IconButton onTouchTap={() => this.props.onAction(enemy.heroId)}>
                    <Clear color={styles.titleStyle.color}/>
                  </IconButton>
                }
              >
                <img src={'/static/images/' + enemy.heroId + '.png'} />
              </GridTile>
            ))}
          </GridList>
        </div>
      </div>
    );
  }
}

LineUp.propTypes = {
  allies: React.PropTypes.array.isRequired,
  enemies: React.PropTypes.array.isRequired,
  onAction: React.PropTypes.func.isRequired,
}
