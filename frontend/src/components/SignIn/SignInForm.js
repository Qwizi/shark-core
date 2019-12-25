import React from 'react';
import { Redirect } from 'react-router-dom';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';

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

    handleFormSubmit(e) {
        e.preventDefault()
        const data = {
            'username': this.state.username,
            'password': this.state.password
        }
        axios.post('http://localhost:8000/api/auth/token/', data)
            .then(res => {
                const data = res.data;
                localStorage.setItem('access_token', data.access)
                this.props.loginUser()
                console.log(localStorage.getItem('access_token'))
            })
        this.setState({fireRedirect: true})
    }

    handleLogOut(e) {
        localStorage.removeItem('access_token')
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