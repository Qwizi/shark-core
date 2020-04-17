import React from 'react';
import {Switch, Route, Redirect} from 'react-router-dom';
import {Forum, Shop, NoMatch, SteamCallback} from './views';
import {CONFIG} from "./config";

const STEAM_CALLBACK = CONFIG.STEAM.CALLBACK;

class Main extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                    <Route exact strict path="/:url*" render={props => <Redirect to={`${props.location.pathname}/`}/>}/>
                    <Route exact path='/'>
                        <Redirect to='/forum/'/>
                    </Route>
                    <Route path='/forum/'>
                        <Forum {...this.props} />
                    </Route>
                    <Route path={STEAM_CALLBACK}>
                        <SteamCallback loginUser={this.props.loginUser}/>
                    </Route>
                    <Route path="/shop/">
                        <Shop {...this.props} />
                    </Route>
                    <Route {...this.props}>
                        <NoMatch/>
                    </Route>
                </Switch>
            </main>
        );
    }
}

export default Main