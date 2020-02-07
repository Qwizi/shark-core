import React from 'react';
import {NavDropdown} from 'react-bootstrap';

class Logged extends React.Component {

    constructor(props) {
        super(props);

        this.handleLogOut = this.handleLogOut.bind(this);
    }

    handleLogOut() {
        this.props.logoutUser();
    }

    render() {
        return (
            <NavDropdown title={`${this.props.user.username}`} id="ucp-dropdown" className="navbar-brand">
                <NavDropdown.Item onClick={this.handleLogOut}>
                    12123
                </NavDropdown.Item>
            </NavDropdown>
        )
    }
}

export default Logged