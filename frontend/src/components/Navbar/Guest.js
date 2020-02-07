import React from 'react';
import {Nav} from 'react-bootstrap';
import {NavLink} from 'react-router-dom';
import {CONFIG} from "../../config";
import querystring from "query-string";

const STEAM_CALLBACK = CONFIG.STEAM.CALLBACK;

class Guest extends React.Component {

    OnSignInClick() {
        const params = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': window.location.origin + STEAM_CALLBACK,
            'openid.realm': window.location.origin,
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',

        };

        window.location = `https://steamcommunity.com/openid/login?openid.ns=${params["openid.ns"]}&openid.mode=${params["openid.mode"]}&openid.return_to=${params["openid.return_to"]}&openid.realm=${params["openid.realm"]}&openid.identity=${params["openid.identity"]}&openid.claimed_id=${params["openid.claimed_id"]}`;
    }

    render() {
        return (
            <Nav>
                <NavLink to="#" className="nav-link" onClick={() => this.OnSignInClick()}>
                    <img
                        src="https://steamcommunity-a.akamaihd.net/public/images/signinthroughsteam/sits_01.png"
                        width="180"
                        height="35"
                        border="0"
                        alt="Steam login"
                    />
                </NavLink>
            </Nav>
        )
    }
}

export default Guest