import React from 'react';
import { Form, Button } from 'react-bootstrap';
import api from '../../api';

const API_URLS = {
    CREATE_USER: '/auth/users/'
}

class SignUpForm extends React.Component
{
    constructor(props) {
        super(props)
        this.state = {
            username: '',
            email: '',
            password: '',
            password2: ''
        }
        this.handleUsernameChange = this.handleUsernameChange.bind(this)
        this.handleEmailChange = this.handleEmailChange.bind(this)
        this.handlePasswordChange = this.handlePasswordChange.bind(this)
        this.handlePassword2Change = this.handlePassword2Change.bind(this)
        this.handleFormSubmit = this.handleFormSubmit.bind(this)
    }

    handleUsernameChange(e) {
        this.setState({username: e.target.value})
    }

    handleEmailChange(e) {
        this.setState({email: e.target.value})
    }

    handlePasswordChange(e) {
        this.setState({password: e.target.value})
    }

    handlePassword2Change(e) {
        this.setState({password2: e.target.value})
    }

    async createUser(data) {
        const response = await api.post(API_URLS.CREATE_USER, data)
        const user = response.data
        return user
    }

    async handleFormSubmit(e) {
        e.preventDefault()
        const { username, email, password } = this.state
        const data = {
            username: username,
            email: email,
            password: password
        }
        this.createUser(data).then(user => {
            console.log(user)
        })
    }

    render() {
        return (
            <div>
                <Form onSubmit={this.handleFormSubmit}>
                    <Form.Group controlId="username">
                        <Form.Label>Username</Form.Label>
                        <Form.Control
                            required
                            type="text"
                            placeholder="Username"
                            value={this.state.username}
                            onChange={this.handleUsernameChange}
                        />
                    </Form.Group>
                    <Form.Group controlId="username">
                        <Form.Label>E-mail</Form.Label>
                        <Form.Control
                            required
                            type="email"
                            placeholder="Email"
                            value={this.state.email}
                            onChange={this.handleEmailChange}
                        />
                    </Form.Group>
                    <Form.Group controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            required 
                            type="password"
                            placeholder="Password"
                            value={this.state.password}
                            onChange={this.handlePasswordChange}
                        />
                    </Form.Group>
                    <Button type="submit" variant="primary">
                        Sign Up
                    </Button>
                </Form>
            </div>
        )
    }
}

export default SignUpForm