import React from "react";
import {withRouter} from "react-router-dom";

class AccountDetail extends React.Component {

    render() {
        const {user, display_role, roles} = this.props;
        return (
            <div className="row">
                <div className="col">
                    <div className="card card-bg">
                        <div className="card-body">
                            <div className="row">
                                <div className="col">
                                    <div className="card card-bg">
                                        <div className="card-body">
                                            <h5 className="card-title">
                                                General details
                                            </h5>
                                            <div className="row">
                                                <div className="col">
                                                    <img src={user.avatar} alt={`${user.username} avatar`}/>
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    Username: <span
                                                    dangerouslySetInnerHTML={{__html: user.formatted_username}}/>
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    Display role: {display_role.name}
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    Roles: {roles.map((role) => <span>{role.name}, </span>)}
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    Posts: {user.posts}
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    Threads: {user.threads}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col">
                                    <div className="card card-bg">
                                        <div className="card-body">
                                            <h5 className="card-title">
                                                Additional details
                                            </h5>
                                            <div className="row">
                                                <div className="col">
                                                    Steamid3: {user.steamid3}
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    Steamid32: {user.steamid32}
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    Steamid64: {user.steamid64}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

AccountDetail.defaultProps = {
    user: {},
    display_role: {id: 0, name: 'User', format: "{username}"},
    roles: []
};

export default withRouter(AccountDetail);