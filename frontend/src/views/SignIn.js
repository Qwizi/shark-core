import React from 'react';
import { Row, Col } from 'react-bootstrap';
import { SignInCard } from '../components/SignIn';

class SignIn extends React.Component
{
    render() {
        return (
            <div>
                <Row className="justify-content-center">
                    <Col xl={4} md={6} sm={12}>
                        <SignInCard {...this.props} />
                    </Col>
                </Row>
            </div>
        );
    }
}

export default SignIn