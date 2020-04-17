import React from "react";
import PropTypes from 'prop-types';
import {Link, Switch, Route, withRouter} from 'react-router-dom';

import {AccountDetail} from "./index";

class Account extends React.Component {
    render() {
        const {match, user} = this.props;
        return (
            <div className="container">
                <div className="row">
                    <div className="col">
                        <ul className="nav nav-tabs">
                            <li className="nav-item">
                                <Link className="nav-link" to={`${match.path}`}>Details</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to={`${match.path}/wallet`}>Wallet</Link>
                            </li>
                        </ul>
                    </div>
                </div>
                <Switch>
                    <Route exact path={`${match.path}`}>
                        <AccountDetail
                            user={user}
                            display_role={user.display_role}
                            roles={user.roles}
                        />
                    </Route>
                    <Route path={`${match.path}/:id`} render={(props) => <div>{props.match.params.id}</div>}/>
                </Switch>
            </div>
        )
    }
}

export default withRouter(Account);