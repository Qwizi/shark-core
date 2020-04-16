import React from "react";
import querystring from "query-string";
import {CONFIG} from "../config"

export default class SteamLoginRedirect extends React.Component
{
    componentDidMount(): void {
        const params = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': window.location.origin + CONFIG.STEAM.CALLBACK,
            'openid.realm': window.location.origin,
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',

        };

        // Tworzymy odpowiednie paramsy
        const paramsFields = querystring.stringify(params);

        setTimeout(function () {
            // Robimy przekierowanie na strone steama
            window.location = CONFIG.STEAM.OPENID_URL + paramsFields;
        }.bind(this), 2500);
    }



    render() {
        return (
            <div className="row">
                <div className="col">
                    <div className="card card-bg">
                        <div className="card-header">
                            Redirect to steam
                        </div>
                        <div className="card-body">
                            Za chwile zostaniesz przeniesiony na strone nalezaca do steama!
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}