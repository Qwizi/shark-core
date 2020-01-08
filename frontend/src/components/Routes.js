import React from 'react';
import { Switch, Route, Redirect, useParams } from 'react-router-dom';
import {
    Home,
    SignIn,
    SignUp,
    Shop,
    Forum,
    NoMatch,
    Thread
} from '../views';

function GuestRoute({ children, ...rest}) {
    return (
        <Route
          {...rest}
          render={({ location }) =>
              !rest.user.logged ? (
              children
            ) : (
              <Redirect
                to={{
                  pathname: "/",
                  state: { from: location }
                }}
              />
            )
          }
        />
      );
}


function PrivateRoute({ children, ...rest }) {

    return (
      <Route
        {...rest}
        render={({ location }) =>
            rest.user.logged ? (
            children
          ) : (
            <Redirect
              to={{
                pathname: "/sign-in/",
                state: { from: location }
              }}
            />
          )
        }
      />
    );
  }

class Main extends React.Component
{
    render() {
        return (
            <main>
                <Switch>
                  <Route exact strict path="/:url*" render={props => <Redirect to={`${props.location.pathname}/`}/>} />
                    <Route exact path='/'>
                        <Home {...this.props} />
                    </Route>
                    <Route path='/forum/' {...this.props}>
                        <Forum {...this.props} />
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
                        <NoMatch />
                    </Route>
                </Switch>
            </main>
        );
    }
}

export default Main