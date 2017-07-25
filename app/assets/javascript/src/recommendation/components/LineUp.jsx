import React from 'react';
import { GridList, GridTile, IconButton } from 'material-ui';
import Clear from 'material-ui/svg-icons/content/clear';

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
    width: '46%',
    display: 'inline-block',
    paddingLeft: '2%',
    paddingRight: '2%',
    paddingTop: '2%',
    textAlign: 'center',
    background: '-moz-linear-gradient(270deg, #E8E8E8 0%, #37474F 80%, #37474F 100%)',
    background: '-webkit-gradient(linear, left top, left bottom, color-stop(0%, #E8E8E8), color-stop(80%, #37474F), color-stop(100%, #37474F))',
    background: '-webkit-linear-gradient(270deg, #E8E8E8 0%, #37474F 80%, #37474F 100%)',
    background: '-o-linear-gradient(270deg, #E8E8E8 0%, #37474F 80%, #37474F 100%)',
    background: '-ms-linear-gradient(270deg, #E8E8E8 0%, #37474F 80%, #37474F 100%)',
    background: 'linear-gradient(180deg, #E8E8E8 0%, #37474F 80%, #37474F 100%)',
  }
};

const MAX_TEAM_SIZE = 5;

export default class LineUp extends React.Component {

  getUndefinedHeroesTiles(heroesDefined) {
    const tiles = [];
    for(let i = 0; i < MAX_TEAM_SIZE-heroesDefined; i++){
      tiles.push((
        <GridTile
          titleStyle={styles.titleStyle}
          titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
          key={i}
        >
          <img src={'/static/images/0.png'} title='Hero to be defined'/>
        </GridTile>
      ));
    }
    return tiles;
  }

  render() {
    return(
      <div>
        <div style={styles.wrapper}>
          ALLIES
          <GridList cols={5} cellHeight={120}>
            {this.props.allies.map((ally) => (
              <GridTile
                style={{borderRadius:'16px'}}
                key={ally.heroId}
                title={ally.localizedName}
                titleStyle={styles.titleStyle}
                titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
                actionIcon={
                  <IconButton
                    iconStyle={styles.smallIcon}
                    style={styles.small}
                    onTouchTap={() => this.props.onAction(ally.heroId)}>
                    <Clear color={styles.titleStyle.color}/>
                  </IconButton>
                }
              >
                <img src={'/static/images/' + ally.heroId + '.png'} />
              </GridTile>
            ))}
            {this.getUndefinedHeroesTiles(this.props.allies.length)}
          </GridList>
        </div>
        <div style={styles.wrapper}>
          ENEMIES
          <GridList style={styles.gridList} cols={5} cellHeight={120}>
            {this.getUndefinedHeroesTiles(this.props.enemies.length)}
            {this.props.enemies.map((enemy) => (
              <GridTile
                style={{borderRadius:'16px'}}
                key={enemy.heroId}
                title={
                  <span style={styles.titleStyle} title={enemy.localizedName}>
                    {enemy.localizedName}
                  </span>
                }
                titleStyle={styles.titleStyle}
                titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
                actionIcon={
                  <IconButton
                    iconStyle={styles.smallIcon}
                    style={styles.small}
                    onTouchTap={() => this.props.onAction(enemy.heroId)}>
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
