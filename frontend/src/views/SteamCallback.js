import React from 'react';
import {withRouter, Redirect} from 'react-router-dom';
import querystring from "query-string";
import api from '../api';
import {CONFIG} from "../config";

const AUTH_ENDPOINT = CONFIG.API.ENDPOINTS.TOKEN.AUTH;

class SteamCallback extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            redirect: false,
            errorMsg: []
        }
    }

    componentDidMount() {
        let params = querystring.parse(this.props.location.search);

        let splitClaimedId = params['openid.claimed_id'].split('/');
        let steamid64 = splitClaimedId[splitClaimedId.length-1];


        let steam_params = {
            'steamid64': steamid64,
            'openid_assoc_handle': params['openid.assoc_handle'],
            'openid_claimed_id': params['openid.claimed_id'],
            'openid_identity': params['openid.identity'],
            'openid_sig': params['openid.sig'],
            'openid_signed': params['openid.signed'],
            'openid_ns': params['openid.ns'],
            'openid_op_endpoint': params['openid.op_endpoint'],
            'openid_return_to': params['openid.return_to'],
            'openid_response_nonce': params['openid.response_nonce'],
        };


        api.post(AUTH_ENDPOINT, params=steam_params)
            .then(response => {
                console.log(response.data);
                this.setState({
                    redirect: true
                })
            })

    }

    render() {
        if (this.state.redirect) {
            return <Redirect to="/forum/"/>
        } else {
            return <Redirect to="/"/>
        }
    }
}

export default withRouter(SteamCallback)