import React from "react";
import querystring from 'query-string';
import {Redirect, withRouter} from 'react-router-dom';

const initialState = {
    fireRedirect: false
};

export default withRouter (class SteamCallback extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;
    }


    componentDidMount(): void {
        const {location, login} = this.props;

        const params = querystring.parse(location.search);

        if (Object.keys(params).length === 0 || !params['openid.claimed_id']) {
            this.redirect();
        } else {
            const steamid64 = this.getSteamid64FromSteamLink(params['openid.claimed_id']);

            const steamParams = {
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

            this.props.login(steamParams);

            this.redirect();
        }
    }

    //Pobieramy steamid z linku, zwrócenego przez steama
    getSteamid64FromSteamLink(claimedId) {
        let splitClaimedId = claimedId.split('/');
        return splitClaimedId[splitClaimedId.length - 1];
    }

    redirect() {
        this.setState({fireRedirect: true});
    }

    render() {
        const {fireRedirect} = this.state;
        return (
            <div>{fireRedirect && (<Redirect to={'/'}/>)}</div>
        );
    }
})