import React from "react";
import PropTypes from "prop-types";
import {Link} from "react-router-dom";

export default class LoggedNav extends React.Component {
    render() {
        const {user, logout} = this.props;
        return (
            <ul className="navbar-nav mr-2">
                <li className="nav-item">
                    <img className="img-fluid mr-2 rounded-pill" src={user.avatar} alt={`${user.username} avatar`}/>
                    <a
                        dangerouslySetInnerHTML={{__html: user.formatted_username}}
                        className="dropdown-toggle"
                        href="#"
                        role="button"
                        id="user-menu"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                        data-reference="parent"
                    />
                    <div className="dropdown-menu user-menu dropdown-menu-lg-right" aria-labelledby="user-menu">
                        <button className="dropdown-item user-menu-item">Profil</button>
                        <div className="dropdown-divider"/>
                        <button className="dropdown-item user-menu-item" onClick={logout()}>Wyloguj</button>
                    </div>
                </li>
            </ul>
        )
    }
}

LoggedNav.propTypes = {
    user: PropTypes.object.isRequired,
    logout: PropTypes.func.isRequired
};