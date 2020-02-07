import React from 'react';

import Guest from "./Guest";
import Logged from "./Logged";

class Nav extends React.Component {
    render() {
        const {user, logoutUser} = this.props;

        if (user.logged) {
            return <Logged user={user} logoutUser={logoutUser}/>
        } else {
            return <Guest/>
        }
    }
}

export default Nav