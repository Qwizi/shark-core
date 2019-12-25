import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import {
    Home,
    SignIn,
    Shop,
    NoMatch
} from '../views/';

function GuestRoute({ children, ...rest}) {
    return (
        <Route
          {...rest}
          render={({ location }) =>
              !rest.isLogged ? (
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
            rest.isLogged ? (
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
                    <Route exact path='/'>
                        <Home />
                    </Route>
                    <GuestRoute path='/sign-in/' {...this.props}>
                        <SignIn {...this.props} />
                    </GuestRoute>
                    <PrivateRoute pathname="/shop/" {...this.props}>
                        <Shop />
                    </PrivateRoute>
                    <Route>
                        <NoMatch />
                    </Route>
                </Switch>
            </main>
        );
    }
}

export default Main