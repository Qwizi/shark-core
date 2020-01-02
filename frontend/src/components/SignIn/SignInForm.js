import React from 'react';
import { Redirect } from 'react-router-dom';
import { Form, Button } from 'react-bootstrap';

class SignInForm extends React.Component
{
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            fireRedirect: false
        }

        this.handleUsernameChange = this.handleUsernameChange.bind(this)
        this.handlePasswordChange = this.handlePasswordChange.bind(this)
        this.handleFormSubmit = this.handleFormSubmit.bind(this)
        this.handleLogOut = this.handleLogOut.bind(this)
    }

    handleUsernameChange(e) {
        this.setState({username: e.target.value})
    }

    handlePasswordChange(e) {
        this.setState({password: e.target.value})
    }

    async handleFormSubmit(e) {
        e.preventDefault()
        const { username, password } = this.state

        await this.props.loginUser(username, password)
        this.setState({fireRedirect: true})

        return Promise.resolve({username: username, password: password})
    }

    handleLogOut(e) {
        this.props.logOutUser()
    }

    render() {

        return (
            <div>
                {this.state.fireRedirect && (
                    <Redirect to={'/'}/>
                )}
            <Form onSubmit={this.handleFormSubmit}>
                <Form.Group controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Username"
                        value={this.state.username}
                        onChange={this.handleUsernameChange}
                    />
                </Form.Group>
                <Form.Group controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                        type="password"
                        placeholder="Password"
                        value={this.state.password}
                        onChange={this.handlePasswordChange}
                    />
                </Form.Group>
                <Button type="submit" variant="primary">
                    Sign In
                </Button>
                <Button varian="danger" onClick={this.handleLogOut}>
                    Sign out
                </Button>
            </Form>
            </div>
        )
    }
}

export default SignInForm