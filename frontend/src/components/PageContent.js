import React from 'react';
import Routes from './Routes';
import Container from 'react-bootstrap/Container';

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

export default class PageContent extends React.Component
{
    render() {
        const { page_name } = this.props
        return (
            <div className="page">
                <div id="banner">
                <div className="context">
                    <PageName page_name={this.props.page_name} page_additonal_name={this.props.page_additonal_name}/>
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