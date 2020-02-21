import React from 'react';
import Routes from './Routes';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import {NavLink} from 'react-router-dom';

const PageName = (props) => {
    if (props.page_additonal_name == null) {
        return (
            <h1>{props.page_name}</h1>
        )
    } else {
        return (
            <h1>{props.page_name} | {props.page_additonal_name}</h1>
        )
    }
}

export default class PageContent extends React.Component {
    render() {
        const {banner} = this.props
        return (
            <div className="page">
                <div id="banner">
                    <div className="context">
                        <PageName page_name={banner.name} page_additonal_name={banner.additional}/>
                    </div>
                    <div className="area">
                        <ul className="circles">
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                        </ul>
                    </div>
                    <Navbar className="navbar-bg2" variant="dark" expand="lg">
                        <Container>
                            <Navbar.Brand></Navbar.Brand>
                            <Navbar.Toggle aria-controls="second-navbar-nav"/>
                            <Navbar.Collapse id="second-navbar-nav">
                                <Nav className="mr-auto">
                                    <NavLink to="/news/" className="nav-link2">Aktualności</NavLink>
                                    <NavLink exact to="/forum/" className="nav-link2">Forum</NavLink>
                                    <NavLink exact to="/shop/" className="nav-link2">Sklep 24/7</NavLink>
                                    <NavLink exact to="/servers/" className="nav-link2">Serwery</NavLink>
                                    <NavLink to="/members/" className="nav-link2">Lista użytkowników</NavLink>
                                </Nav>
                            </Navbar.Collapse>
                        </Container>
                    </Navbar>
                </div>
                <>

                </>
                <Container fluid="true" className="page-content">
                    <Routes {...this.props}/>
                </Container>
            </div>
        );
    }
}