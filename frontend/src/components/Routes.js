import React from 'react';
import {Switch, Route, Redirect} from 'react-router-dom';
import {
    Home,
    SignIn,
    SignUp,
    Shop,
    Forum,
    NoMatch
} from '../views';
import Steam from '../views/Steam';
import SteamCallback from "../views/SteamCallback";

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

class Main extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                    <Route exact strict path="/:url*" render={props => <Redirect to={`${props.location.pathname}/`}/>}/>
                    <Route exact path='/'>
                        <Home {...this.props} />
                    </Route>
                    <Route path='/forum/' {...this.props}>
                        <Forum {...this.props} />
                    </Route>
                    <Route path='/auth/steam/' {...this.props}>
                        <Steam {...this.props} />
                    </Route>
                    <Route path='/steam_callback/' {...this.props}>
                        <SteamCallback {...this.props} />
                    </Route>
                    <GuestRoute path='/sign-in/' {...this.props}>
                        <SignIn {...this.props} />
                    </GuestRoute>
                    <GuestRoute path='/sign-up/' {...this.props}>
                        <SignUp {...this.props} />
                    </GuestRoute>
                    <PrivateRoute pathname="/shop/" {...this.props}>
                        <Shop {...this.props} />
                    </PrivateRoute>
                    <Route {...this.props}>
                        <NoMatch/>
                    </Route>
                </Switch>
            </main>
        );
    }
}

export default Main