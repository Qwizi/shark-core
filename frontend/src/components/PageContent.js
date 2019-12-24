import React from 'react';
import Main from './Main';
import Container from 'react-bootstrap/Container';

export default class PageContent extends React.Component
{
    render() {
        return (
            <div>
                <Container fluid="true" className="container-padding">
                    <Main {...this.props}/>
                </Container>
            </div>
        );
    }
}