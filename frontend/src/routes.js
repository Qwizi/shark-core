import React from "react";
import PropTypes from 'prop-types';
import {Switch, Route, Redirect} from 'react-router-dom';
import {Account, Forum, News, SteamCallback, SteamLoginRedirect} from "./views";
import {CONFIG} from "./config";

class Routes extends React.Component
{
    render() {
        const steamCallbackEndpoint = CONFIG.STEAM.CALLBACK || '/auth/steam/callback/';
        const steamRedirectEndpoint = CONFIG.STEAM.REDIRECT || '/auth/steam/redirect/';
        return (
            <Switch>
                <Route exact path="/">
                    <News/>
                </Route>

                <Route path="/news">
                    <News/>
                </Route>

                <Route path="/forum">
                    <Forum user={this.props.user} />
                </Route>

                <Route path="/account">
                    <Account user={this.props.user}/>
                </Route>

                <Route path={`${steamCallbackEndpoint}`}>
                    <SteamCallback login={this.props.login}/>
                </Route>

                <Route path={`${steamRedirectEndpoint}`}>
                    <SteamLoginRedirect/>
                </Route>
            </Switch>
        )
    }
}

Routes.propTypes = {
    logged: PropTypes.bool.isRequired,
    user: PropTypes.object.isRequired,
};

export default Routes;