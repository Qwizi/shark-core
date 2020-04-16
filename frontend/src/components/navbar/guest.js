import React from "react";
import {Link} from "react-router-dom";
import {Redirect} from 'react-router-dom';

import querystring from "query-string";

import {CONFIG} from "../../config";

const initialState = {
    fireRedirect: false
};

export default class GuestNav extends React.Component {

    constructor(props) {
        super(props);

        this.state = initialState;

        this.handleSteamBtnClick = this.handleSteamBtnClick.bind(this);
    }

    handleSteamBtnClick() {
        this.setState({fireRedirect: true})
    }

    render() {
        const {fireRedirect} = this.state;
        return (
            <ul className="navbar-nav mr-2">
                <li className="nav-item">
                    <Link className="nav-link" to="/auth/steam/callback/">
                        <img
                            src="https://steamcommunity-a.akamaihd.net/public/images/signinthroughsteam/sits_01.png"
                             width="180"
                            height="35"
                            border="0"
                            onClick={this.handleSteamBtnClick}
                            alt={'Login via steam'}
                        />
                    </Link>
                </li>
                {fireRedirect && (<Redirect to={CONFIG.STEAM.REDIRECT}/>)}
            </ul>
        )
    }
}