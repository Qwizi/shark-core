import React from 'react';
import './App.css';
import { NavBar } from './navbar';
import PageContent from './PageContent';
import { BrowserRouter as Router } from 'react-router-dom'
import api from '../api';

const API_URLS = {
  USER: '/accounts/me/',
  LOGIN: '/token/auth/',
  REFRESH: '/token/refresh/'
}

class App extends React.Component
{
  constructor(props) {
    super(props);
    this.state = {
      user: {
        logged: localStorage.getItem('access_token') && localStorage.getItem('refresh_token') ? true : false,
        pk: null,
        username: null,
        email: null,
        display_group: null,
        is_active: null,
        is_staff: null,
        date_joined: null
      },
      page_name: 'Home',
      page_additonal_name: null
    }

    this.loginUser = this.loginUser.bind(this)
    this.logOutUser = this.logOutUser.bind(this)
    this.getUserData = this.getUserData.bind(this)
    this.setPageName = this.setPageName.bind(this)
    this.setPageAdditionalName = this.setPageAdditionalName.bind(this)
  }

  async getUserData() {
    const access_token = localStorage.getItem('access_token')
    const payload = {
      headers: {
        Authorization: `Bearer ${access_token}`
      }
    }
    const response = await api.get(API_URLS.USER, payload)
    const user = response.data
    return Promise.resolve(user)
  }

  async getNewToken(refresh_token) {
    const response = await api.post(API_URLS.REFRESH, {refresh: refresh_token})
    const { access } = response.data
    return Promise.resolve(access)
  }

  async componentDidMount() {
    const { logged } = this.state.user
    if (logged) {

      const refresh_token = localStorage.getItem('refresh_token')
      this.getUserData()  
        .then(user => {
          this.setState((state) => ({
            user: {logged: state.user.logged, ...user}
          }))
        })
        .catch(error => {
          if (error.response.status === 401) {
            this.getNewToken(refresh_token)
              .then(new_token => {
                localStorage.setItem('access_token', new_token)
                this.getUserData()  
                .then(user => {
                  this.setState((state) => ({
                    user: {logged: state.user.logged, ...user}
                  }))
                })
              })
              .catch(error => {
                if (error.response.status === 401) {
                  this.logOutUser()
                }
              })

          }
        })

      // const user = this.getUserData()
      //this.setState((state) => ({
       //user: {logged: state.user.logged, ...user}
     //}))
    }
  }

  async getAuthToken(username, password) {
    const data = {
      username: username,
      password: password
    }
    const response = await api.post(API_URLS.LOGIN, data)
    const { access, refresh } = response.data

    const return_data = {
      access: access,
      refresh: refresh
    }

    return Promise.resolve(return_data)
  }

  async loginUser(username, password) {
    this.getAuthToken(username, password).then(data => {

      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      
      //this.getUserData().then(user => {
      //  const user_data = {logged: true, ...user}
      //  this.setState({user: user_data})
      //  return Promise.resolve(user)
      // })
    })
  }

  logOutUser() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    this.setState({user: {}})
  }

  setPageName(page_name) {
    this.setState({
        page_name: page_name
    })
  }

  setPageAdditionalName(page_name) {
    this.setState({
        page_additonal_name: page_name
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
          setPageName={this.setPageName}
          page_name={this.state.page_name}
          setPageAdditionalName={this.setPageAdditionalName}
          page_additonal_name={this.state.page_additonal_name}
        />
      </Router>
    );
  }
}

export default App;
