import React from 'react';
import './App.css';
import NavBar from './NavBar';
import PageContent from './PageContent';
import { BrowserRouter as Router } from 'react-router-dom'
import axios from 'axios'

class App extends React.Component
{
  constructor(props) {
    super(props);
    this.state = {
      isLogged: localStorage.getItem('access_token') ? true : false,
    }

    this.loginUser = this.loginUser.bind(this)
    this.logOutUser = this.logOutUser.bind(this)  
  }

  componentDidMount() {
      const { isLogged } = this.state
      if (isLogged && !sessionStorage.getItem('user_data')) {
        sessionStorage.setItem('user_data', '125')
      }
      console.log(sessionStorage.getItem('user_data'))
  }

  loginUser() {
    this.setState(state => ({
      isLogged: true
    }));
    //this.forceUpdate()
  }

  logOutUser() {
    this.setState(state => ({
      isLogged: false
    }));
    sessionStorage.clear()
    //this.forceUpdate()
  }

  render() {
    return (
      <Router>
        <NavBar/>
        <PageContent
          isLogged={this.state.isLogged}
          loginUser={this.loginUser}
          logOutUser={this.logOutUser}
        />
      </Router>
    );
  }
}

export default App;
