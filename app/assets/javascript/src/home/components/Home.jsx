import React from 'react';
import { Avatar, Card, CardHeader, CardMedia, CardTitle, CardText, CardActions,
  FlatButton, IconButton, FontIcon, Tabs, Tab } from 'material-ui';
import SwipeableViews from 'react-swipeable-views';
import ContentHolder from '../../components/ContentHolder.jsx';

export default class Home extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      slideIndex: 0,
      userChangedTab: false,
    };
  }

  componentDidMount(){
    setTimeout(this.forward.bind(this), 3000);
  }

  componentDidUpdate() {
    setTimeout(this.forward.bind(this), 3000);
  }

  forward(){
    if (this.state.userChangedTab) return;
    let next = this.state.slideIndex == 3 ? 0 : this.state.slideIndex + 1;
    this.setState({
      slideIndex: next,
    });
  }

  handleChange(value) {
    this.setState({
      slideIndex: value,
      userChangedTab: true,
    });
  }

  render() {
    return (
      <ContentHolder style={{ width: "90%" }}>
        <Tabs
          onChange={ this.handleChange.bind(this) }
          value={ this.state.slideIndex } >
          <Tab label="What" value={0} />
          <Tab label="How" value={1} />
          <Tab label="Who" value={2} />
          <Tab label="Help" value={3} />
        </Tabs>
        <SwipeableViews
          animateHeight={ true }
          index={ this.state.slideIndex }
          onChangeIndex={ this.handleChange.bind(this) }>
          <div>
            <Card>
              <CardMedia
                overlay={ <CardTitle title="What is House o' Dota?" /> } >
                <div className="crop slide1">
                  <img src="/static/images/slide1.png" />
                </div>
              </CardMedia>
              <CardText>
                House of Dota is a place where you can get several kinds of insights regarding the
                game current meta. What are the heroes most picked? What are the most powerful hero combos?
                Besides, we have a recommendation system in order to help you choosing the best hero
                for your line-up.
              </CardText>
            </Card>
          </div>
          <div>
            <Card>
              <CardMedia overlay={ <CardTitle title="How does it work?"/> }>
                <div className="crop slide2">
                  <img src="/static/images/slide2.png" />
                </div>
              </CardMedia>
              <CardText>
                We periodically collect valid and very high matches from Steam API. From this data,
                we analyze and run our machine learning algorithms in order to better understand the meta
                and make predictions and statistical analysis of the game.
              </CardText>
            </Card>
          </div>
          <div>
            <Card>
              <CardMedia overlay={<CardTitle title="Who’s behind House o' Dota?" />} >
                <div className="crop slide3">
                  <img src="/static/images/slide3.png" />
                </div>
              </CardMedia>
              <CardHeader
                title="Lucas Hanke"
                subtitle="Master Student @UFMG and Consultant Developer @ThoughtWorks"
                avatar={'https://avatars3.githubusercontent.com/u/5628437?v=3&s=460'}
                />
              <CardText>
                Hello, I'm Lucas! I'm a master student at Universidade Federal de Minas Gerais, Brazil
                and House of Dota is the result of my dissertation project! I am passionate about technology, data science,
                machine learning and (of course) Dota 2. I am currently also a consultant developer at ThoughtWorks.
              </CardText>
              <CardActions>
                <FlatButton
                  label="Twitter"
                  labelPosition="before"
                  href="https://twitter.com/lucashanke"
                  primary={true}
                  icon={<FontIcon className="muidocs-icon-custom-twitter" />}
                  />
                <FlatButton
                  label="GitHub"
                  href="https://github.com/lucashanke"
                  secondary={true}
                  icon={<FontIcon className="muidocs-icon-custom-github" />}
                  />
              </CardActions>
            </Card>
          </div>
          <div>
            <Card>
              <CardMedia
                overlay={
                  <CardTitle
                    title="Help is always welcome!"
                    subtitle={
                      <a style={{ color:'white' }}
                        href="https://www.youtube.com/watch?v=9qbp2F-wN5M">
                        '"Giff me support"'
                      </a>
                    }
                  />
                }>
                <div className="crop slide4">
                  <img src="/static/images/slide4.jpg" />
                </div>
              </CardMedia>
              <CardText>
                Please feel free to contribute to the project on <a href="https://github.com/lucashanke/houseofdota">github.com/lucashanke/houseofdota</a>.
                <br></br><br></br>
                Copyright Notice
                <br></br>
                Dota 2 is a registered trademark of Valve Corporation.
              </CardText>
              <CardActions>
                <FlatButton
                  label="House of Dota @Github"
                  href="https://github.com/lucashanke/houseofdota"
                  secondary={true}
                  icon={<FontIcon className="material-icons">group_work</FontIcon>} />
              </CardActions>
            </Card>
          </div>
        </SwipeableViews>
      </ContentHolder>
    );
  }
}
