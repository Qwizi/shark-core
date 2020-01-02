import React from 'react';
import './App.css';
import { NavBar } from './navbar';
import PageContent from './PageContent';
import { BrowserRouter as Router } from 'react-router-dom'
import api from '../api';

const API_URLS = {
  USER: '/auth/users/me/',
  LOGIN: '/auth/token/login/',
  LOGOUT: '/auth/token/logout/'
}

class App extends React.Component
{
  constructor(props) {
    super(props);
    this.state = {
      user: {
        logged: localStorage.getItem('auth_token') ? true : false,
        pk: null,
        username: null,
        email: null,
        display_group: null,
        is_active: null,
        is_staff: null,
        date_joined: null
      }
    }

    this.loginUser = this.loginUser.bind(this)
    this.logOutUser = this.logOutUser.bind(this)
    this.getUserData = this.getUserData.bind(this)
  }

  async getUserData() {
    const auth_token = localStorage.getItem('auth_token')
    const payload = {
      headers: {
        Authorization: `Token ${auth_token}`
      }
    }
    const response = await api.get(API_URLS.USER, payload)

    const user = response.data
    return Promise.resolve(user)
  }

  async componentDidMount() {
    const { logged } = this.state.user
    if (logged) {
      const user = await this.getUserData()
      this.setState((state) => ({
        user: {logged: state.user.logged, ...user}
      }))
    }
  }

  async getAuthToken(username, password) {
    const data = {
      username: username,
      password: password
    }
    const response = await api.post(API_URLS.LOGIN, data)
    const { auth_token } = response.data;
    return Promise.resolve(auth_token)
  }

  async removeAuthToken() {
    const auth_token = localStorage.getItem('auth_token')
    const data = {
      headers: {
        Authorization: `Token ${auth_token}`
      }
    }
    await api.post(API_URLS.LOGOUT, null, data)
  }

  async loginUser(username, password) {
    this.getAuthToken(username, password).then(auth_token => {
      localStorage.setItem('auth_token', auth_token)
      this.getUserData().then(user => {
        const user_data = {logged: true, ...user}
        this.setState({user: user_data})
        const data = {
          auth_token: auth_token,
          user: user_data
        }
        return Promise.resolve(data)
      })
    })
  }

  logOutUser() {
    const auth_token = localStorage.getItem('auth_token')
    this.removeAuthToken(auth_token).then(data => {
      localStorage.removeItem('auth_token')
      this.setState({user: {}})
    })
  }

  render() {
    return (
      <Router>
        <NavBar
          logOutUser={this.logOutUser}
          user={this.state.user}
        />
        <PageContent
          loginUser={this.loginUser}
          logOutUser={this.logOutUser}
          user={this.state.user}
        />
      </Router>
    );
  }
}

export default App;
