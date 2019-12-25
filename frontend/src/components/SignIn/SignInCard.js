import React from 'react';
import { Card } from 'react-bootstrap'
import SignInForm from './SignInForm';

class SignInCard extends React.Component
{
    render() {
        return (
            <Card className="h-100">
                <Card.Header className="sign-in-card text-center">
                    <h1>Sign-in</h1>
                </Card.Header>
                <Card.Body className="bonus-card">
                    <SignInForm {...this.props} />
                </Card.Body>
            </Card>
        )
    }
}

export default SignInCard