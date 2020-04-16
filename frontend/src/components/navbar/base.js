import React from 'react';
import PropTypes from "prop-types";
import {Link} from "react-router-dom";

import GuestNav from "./guest";
import LoggedNav from "./logged";

export default class Navbar extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {logged, logout, user} = this.props;

        const nav = logged ? <LoggedNav user={user} logout={logout}/> : <GuestNav/>;

        return (
            <nav className="navbar navbar-expand-lg navbar-dark navbar-bg ">
                <Link className="navbar-brand" to="/">SharkCore</Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"/>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <Link className="nav-link" to="/news/">News</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/forum/">Forum</Link>
                        </li>
                    </ul>
                    {nav}
                </div>
            </nav>
        )
    }
}

Navbar.propTypes = {
    logged: PropTypes.bool.isRequired,
    logout: PropTypes.func.isRequired,
    user: PropTypes.object.isRequired
};