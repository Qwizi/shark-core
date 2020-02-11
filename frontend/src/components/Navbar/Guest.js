import React from 'react';
import {Nav} from 'react-bootstrap';
import {NavLink} from 'react-router-dom';
import {CONFIG} from "../../config";
import querystring from "query-string";

const STEAM_CALLBACK = CONFIG.STEAM.CALLBACK;
const STEAM_OPENID_LINK = CONFIG.STEAM.OPENID_URL;

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

        // Tworzymy odpowiednie paramsy
        const paramsFields = querystring.stringify(params);

        // Robimy przekierowanie na strone steama
        window.location = STEAM_OPENID_LINK + paramsFields;
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