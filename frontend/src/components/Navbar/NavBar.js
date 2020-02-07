import React from 'react';
import {Navbar, Nav as BoostrapNav} from 'react-bootstrap';
import {NavLink} from 'react-router-dom';

import Nav from "./Nav";

class NavBar extends React.Component {

    render() {
        return (
            <Navbar className="navbar-bg" variant="dark" expand="lg">
                <Navbar.Brand>
                    <NavLink className="navbar-brand" to="/">SharkCore</NavLink>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <BoostrapNav className="mr-auto">
                        <NavLink exact to="/forum/" className="nav-link">Forum</NavLink>
                        <NavLink exact to="/shop/" className="nav-link">Shop</NavLink>
                    </BoostrapNav>
                    <Nav {...this.props}/>
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default NavBar