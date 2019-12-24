import React from 'react';
import {Switch, Route } from 'react-router-dom';
import Home from '../views/Home';
import SignIn from '../views/SignIn';
import Shop from '../views/Shop';

export default class Main extends React.Component
{
    render() {
        return (
            <main>
                <Switch>
                    <Route 
                        exact 
                        path='/' 
                        render={(props) => (<Home {...this.props} />)}
                    />
                    <Route path='/sign-in/' component={SignIn}/>
                    <Route path='/shop/' component={Shop}/>
                </Switch>
            </main>
        );
    }
}