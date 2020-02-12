import React from 'react';
import {Switch, Route, Redirect} from 'react-router-dom';
import {
    Shop,
    Forum,
    NoMatch
} from './views';
import SteamCallback from "./views/SteamCallback";
import {CONFIG} from "./config";

const STEAM_CALLBACK = CONFIG.STEAM.CALLBACK;
/*


function GuestRoute({children, ...rest}) {
    return (
        <Route
            {...rest}
            render={({location}) =>
                !rest.user.logged ? (
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/",
                            state: {from: location}
                        }}
                    />
                )
            }
        />
    );
}


function PrivateRoute({children, ...rest}) {

    return (
        <Route
            {...rest}
            render={({location}) =>
                rest.user.logged ? (
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/sign-in/",
                            state: {from: location}
                        }}
                    />
                )
            }
        />
    );
}
*/

class Main extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                    <Route exact strict path="/:url*" render={props => <Redirect to={`${props.location.pathname}/`}/>}/>
                    <Route exact path={'/'}>
                        <Redirect to='/forum/'/>
                    </Route>
                    <Route exact path='/forum/' {...this.props}>
                        <Forum {...this.props} />
                    </Route>
                    <Route path='/auth/steam/callback/'>
                        <SteamCallback loginUser={this.props.loginUser} />
                    </Route>
                    <Route path="/shop/" {...this.props}>
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