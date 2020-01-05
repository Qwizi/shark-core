import React from 'react';
import Routes from './Routes';
import Container from 'react-bootstrap/Container';

export default class PageContent extends React.Component
{
    render() {
        const { page_name } = this.props
        return (
            <div className="page">
                <div id="banner">
                <div className="context">
                    <h1>{page_name}</h1>
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
                    </div>
                <Container fluid="true" className="page-content">
                        <Routes {...this.props}/>
                </Container>
            </div>
        );
    }
}