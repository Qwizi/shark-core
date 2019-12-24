import React from 'react';
import Navbar from 'react-bootstrap/Navbar';

export default class NavBar extends React.Component
{
    render() {
        return (
            <Navbar className="navbar-bg" variant="dark">
                <Navbar.Brand href="#home">
                    SharkCore
                </Navbar.Brand>
            </Navbar>
        );
    }
}