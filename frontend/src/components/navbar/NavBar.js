import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

import GuestNav from './GuestNav';

class NavBar extends React.Component
{
   
    render() {

        const { logOutUser } = this.props
        const { logged } = this.props.user

        return (
            <Navbar className="navbar-bg" variant="dark" expand="lg">
                <Navbar.Brand>
                    <NavLink className="navbar-brand" to="/">SharkCore</NavLink>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <NavLink exact to="/forum/" className="nav-link">Forum</NavLink>
                    <NavLink exact to="/shop/" className="nav-link">Shop</NavLink>
                </Nav>
                <GuestNav logged={logged} logOutUser={logOutUser} />
            </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default NavBar