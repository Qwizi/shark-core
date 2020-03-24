import React from 'react';
import {Navbar, Nav as BoostrapNav} from 'react-bootstrap';
import {NavLink} from 'react-router-dom';

import Nav from "./Nav";

class NavBar extends React.Component {
    componentDidMount() {
        let navbar = document.querySelector('.navbar-bg')
        window.addEventListener('scroll', function(e) {
            let last_scroll_position = window.scrollY;
            if (last_scroll_position > 100) {
                navbar.classList.add('affix')
            } else {
                navbar.classList.remove('affix')
            }
        })
    }

    render() {
        return (
            <Navbar className="navbar-bg" variant="dark" expand="lg" fixed="top">
                <Navbar.Brand>
                    <NavLink className="navbar-brand" to="/">SharkCore</NavLink>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <BoostrapNav className="mr-auto">
                    </BoostrapNav>
                    <Nav {...this.props}/>
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default NavBar