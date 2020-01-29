import React from 'react';
import { Nav, NavDropdown } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

class GuestNav extends React.Component
{
    constructor(props) {
        super(props);

        this.handleLogOut = this.handleLogOut.bind(this)
    }

    handleLogOut(e) {
        this.props.logOutUser()
    }

    OnSignInClick() {
        const params = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': "http://localhost:3000/steam_callback/",
            'openid.realm': 'http://localhost:3000/',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',

        };

        window.location = `https://steamcommunity.com/openid/login?openid.ns=${params["openid.ns"]}&openid.mode=${params["openid.mode"]}&openid.return_to=${params["openid.return_to"]}&openid.realm=${params["openid.realm"]}&openid.identity=${params["openid.identity"]}&openid.claimed_id=${params["openid.claimed_id"]}`;
    }


    render() {
        const { logged } = this.props

        if (!logged) {
            return (
                <Nav>
                    <NavLink to="#" className="nav-link" onClick={() => this.OnSignInClick()}>
                        <img src="https://steamcommunity-a.akamaihd.net/public/images/signinthroughsteam/sits_01.png" width="180" height="35" border="0"/>
                    </NavLink>
                </Nav>
            )
        } else {
            return (
                <NavDropdown title="ucp" id="ucp-dropdown" className="navbar-brand">
                    <NavDropdown.Item onClick={this.handleLogOut}>
                        12123
                    </NavDropdown.Item>
                </NavDropdown>
            )
        }
    }
}

export default GuestNav