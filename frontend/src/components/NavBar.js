import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

export default class NavBar extends React.Component
{
    render() {
        return (
            <Navbar className="navbar-bg" variant="dark" expand="lg">
                <Navbar.Brand>
                    <NavLink className="navbar-brand" to="/">SharkCore</NavLink>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <NavLink exact to="/" className="nav-link">Home</NavLink>
                    <NavLink exact to="/shop/" className="nav-link">Shop</NavLink>
                </Nav>
                <Nav>
                    <NavLink exact to="/sign-in/" className="nav-link">Sign in</NavLink>
                    <NavLink exact to="/sign-up/" className="nav-link">Sign up</NavLink>
                </Nav>
            </Navbar.Collapse>
            </Navbar>
        );
    }
}