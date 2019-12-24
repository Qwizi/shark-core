import React from 'react'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default class Home extends React.Component
{
    render() {
        return (
            <div>
                <Row className="justify-content-center">
                    <Col md="auto"><h1>Home page</h1> {this.props.test}</Col>
                </Row>
            </div>
        )
    }
}