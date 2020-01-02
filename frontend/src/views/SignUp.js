import React from 'react'
import { Row, Col } from 'react-bootstrap';
import { SignUpCard } from '../components/SignUp';

class SignUp extends React.Component
{
    render() {
        return (
            <Row className="justify-content-center">
                <Col xl={4} md={6} sm={12}>
                    <SignUpCard {...this.props }/>
                </Col>
            </Row>
        )
    }
}

export default SignUp