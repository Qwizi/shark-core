import React from 'react';
import {NavDropdown, Image} from 'react-bootstrap';
import Parser from 'html-react-parser';

class Logged extends React.Component {

    constructor(props) {
        super(props);

        this.handleLogOut = this.handleLogOut.bind(this);
    }

    handleLogOut() {
        this.props.logoutUser();
    }

    render() {
        let formatted_username = this.props.user.formatted_username;
        formatted_username = String(formatted_username)
        console.log(String(formatted_username))
        return (
            <div>

                <Image src={this.props.user.avatar} roundedCircle />
                <NavDropdown title={Parser(formatted_username)} id="ucp-dropdown" className="navbar-brand">
                    <NavDropdown.Item>
                        Profil
                    </NavDropdown.Item>
                    <NavDropdown.Item>
                        Ustawienia
                    </NavDropdown.Item>
                    <NavDropdown.Item onClick={this.handleLogOut}>
                        Wyloguj
                    </NavDropdown.Item>
                </NavDropdown>
            </div>
        )
    }
}

export default Logged