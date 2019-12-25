import React from 'react';
import { Row, Col } from 'react-bootstrap';

class NoMatch extends React.Component
{
    render() {
        return  (
            <Row className="justify-content-center">
                <Col md="auto"><h1>404 - NOT FOUND</h1></Col>
            </Row>
        )
    }
}

export default NoMatch