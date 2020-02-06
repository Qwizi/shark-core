import React from 'react';
import {Form, Button} from 'react-bootstrap';
import {CONFIG} from "../config";

const STEAM_CALLBACK = CONFIG.STEAM.CALLBACK;

class Steam extends React.Component {
    onFormSubmit() {
        console.log('wyslano')
        const params = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': window.location.origin + STEAM_CALLBACK,
            'openid.realm': window.location.origin,
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',

        }

        window.location = `https://steamcommunity.com/openid/login?openid.ns=${params["openid.ns"]}&openid.mode=${params["openid.mode"]}&openid.return_to=${params["openid.return_to"]}&openid.realm=${params["openid.realm"]}&openid.identity=${params["openid.identity"]}&openid.claimed_id=${params["openid.claimed_id"]}`
        // window.location = 'http://localhost:8000/auth/login/steam/'
    }

    render() {
        return (
            <Button onClick={() => this.onFormSubmit()}>
                Zaloguj sie przez steama
            </Button>
        )
    }
}

export default Steam