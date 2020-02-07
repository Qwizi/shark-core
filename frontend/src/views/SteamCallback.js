import React from 'react';
import {Redirect, withRouter} from 'react-router-dom';
import querystring from "query-string";

class SteamCallback extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            redirect: false,
        };

        this.setRedirectState = this.setRedirectState.bind(this);
    }

    componentDidMount() {
        let params = querystring.parse(this.props.location.search);

        const steamid64 = this.getSteamid64FromSteamLink(params['openid.claimed_id']);

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

        // Jezeli logowanie przez steam powiodlo się logujemy uzytkownika w naszym systemie
        this.props.loginUser(steam_params);
        this.setRedirectState(true);

    }

    /*
     * Ustawiamy stan redirect
     */
    setRedirectState(value) {
        this.setState({
            redirect: value
        })
    }

    /*
     * Pobieramy steamid z linku, zwrócenego przez steama
     */
    getSteamid64FromSteamLink(claimedId) {
        let splitClaimedId = claimedId.split('/');
        return splitClaimedId[splitClaimedId.length - 1];
    }

    render() {
        if (this.state.redirect) {
            return <Redirect to="/"/>
        } else {
            return <></>
        }
    }
}

export default withRouter(SteamCallback)