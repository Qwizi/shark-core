import React from 'react';
import './App.css';
import NavBar from './NavBar';
import PageContent from './PageContent';

class App extends React.Component
{
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      user: {},
      categories: []
    }
  }

  render() {
    return (
      <div>
        <NavBar/>
        <PageContent />
      </div>
    );
  }
}

export default App;
