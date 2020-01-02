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

    render() {
        const { logged } = this.props

        if (!logged) {
            return (
                <Nav>
                    <NavLink exact to="/sign-in/" className="nav-link">Sign in</NavLink>
                    <NavLink exact to="/sign-up/" className="nav-link">Sign up</NavLink>
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