import React from 'react';
import { Card } from 'react-bootstrap';
import SignUpForm from './SignUpForm';

class SignUpCard extends React.Component
{
    render() {
        return (
            <Card className="h-100">
                <Card.Header className="sign-in-card text-center">
                    <h1>Sign-up</h1>
                </Card.Header>
                <Card.Body className="bonus-card">
                    <SignUpForm {...this.props}/>
                </Card.Body>
            </Card>
        )
    }
}

export default SignUpCard