import React from 'react';
import './App.css';
import {NavBar} from './components/Navbar';
import PageContent from './PageContent';
import {BrowserRouter as Router} from 'react-router-dom'
import api from './api';
import {CONFIG} from "./config";

const TOKEN_ENDPOINT = CONFIG.API.ENDPOINTS.TOKEN.AUTH;
const REFRESH_ENDPOINT = CONFIG.API.ENDPOINTS.TOKEN.REFRESH;
const ACCOUNTS_ME_ENDPOINT = CONFIG.API.ENDPOINTS.ACCOUNTS.ME;


class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: {
                logged: !!localStorage.getItem('access_token'),
                username: null,
                steamid64: null,
                steamid32: null,
                steamid3: null,
                display_group: null,
                is_active: null,
                is_staff: null,
                date_joined: null
            },
            banner: {
                name: 'Forum',
                additional: null
            },
            banner_page_name: 'Forum',
            banner_additional_page_name: null
        };

        this.setUserState = this.setUserState.bind(this);
        this.setBannerPageName = this.setBannerPageName.bind(this);
        this.setBannerPageAdditionalName = this.setBannerPageAdditionalName.bind(this);
        this.logoutUser = this.logoutUser.bind(this);
        this.loginUser = this.loginUser.bind(this);
        this.logoutUserState = this.logoutUserState.bind(this);
    }

    async componentDidMount() {
        const {user} = this.state;

        if (user.logged) {
            this.getUserData().then(userData => {
                this.setUserState(userData);
            }).catch(error => {
                console.log(error.response);
                if (error.response.status === 401) {
                    this.removeLocalTokens();
                    this.logoutUserState();
                }
            })
        }
    }

    /*
     * Logujemy uzytkownika
     */
    loginUser = async (params) => {
        // Pobieramy tokeny z api
        this.getAuthTokens(params).then(data => {
            // Ustawiamy lokalne tokeny
            this.setLocalTokens(data.access, data.refresh);
            //Pobieramy dane zalogowanego uzytkownika
            this.getUserData().then(userData => {
                // Uzupleniamy stan/obiek zalogowanego uzytkownika
                this.setUserState(userData, true);
            })
        })
    }

    /*
     * Wylogowujemy uzytkownika
     */
    logoutUser() {
        // Usuwamy lokalne tokeny
        this.removeLocalTokens();
        this.logoutUserState();
    }


    /*
     ******************************************************************************
     **************************ZAPYTANIA DO API************************************
     ******************************************************************************
     */

    /*
     * Pobieramy tokeny z api
     */
    getAuthTokens = async (params) => {
        const response = await api.post(TOKEN_ENDPOINT, params);
        return response.data;
    };

    /*
     * Pobieramy dane zalogowanego uzytkownika
     */
    getUserData = async () => {
        const authorizationHeader = this.createAuthorizationHeader();
        const response = await api.get(ACCOUNTS_ME_ENDPOINT, {
            headers: authorizationHeader
        });

        return response.data;
    };


    /*
     ******************************************************************************
     ********************************POMOCNICZE METODY*****************************
     ******************************************************************************
     */

    /*
     * Uzupelniany obiekt/stan uzytkownika
     */
    setUserState(userData, logged = null) {
        this.setState(function (state) {
            return {
                user: {
                    logged: logged === null ? state.user.logged : logged,
                    username: userData.username,
                    steamid64: userData.steamid64,
                    steamid32: userData.steamid32,
                    steamid3: userData.steamid3,
                    display_group: userData.display_group,
                    is_active: userData.is_active,
                    is_staff: userData.is_staff,
                    date_joined: userData.date_joined
                }
            }
        });

    }

    logoutUserState() {
        this.setState({
            user: {
                logged: false,
                username: null,
                steamid64: null,
                steamid32: null,
                steamid3: null,
                display_group: null,
                is_active: null,
                is_staff: null,
                date_joined: null
            }
        })
    }

    /*
     * Ustawiamy access token w localStorage
     */
    setLocalAccessToken(accessToken) {
        localStorage.setItem('access_token', accessToken);
    }

    /*
     * Ustawiamy refresh token w localStorage
     */
    setLocalRefreshToken(refreshToken) {
        localStorage.setItem('refresh_token', refreshToken);
    }

    /*
     * Ustawiamy tokeny w localStorage
     */
    setLocalTokens(accessToken, refreshToken) {
        this.setLocalAccessToken(accessToken);
        this.setLocalRefreshToken(refreshToken);
    }

    /*
     * Pobieramy access token z localStorage
     */
    getLocalAccessToken() {
        return localStorage.getItem('access_token');
    }

    /*
     * Pobieramy refresh token z localStorage
     */
    getLocalRefreshToken() {
        return localStorage.getItem('refresh_token');
    }


    /*
     * Usuwamy access token z localStorage
     */
    removeLocalAccessToken() {
        localStorage.removeItem('access_token');
    }

    /*
     * Usuwamy refresh token z localStorage
     */
    removeLocalRefreshToken() {
        localStorage.removeItem('refresh_token');
    }

    /*
     * Uswamy access i refresh token z localStorage
     */
    removeLocalTokens() {
        this.removeLocalAccessToken();
        this.removeLocalRefreshToken();
    }

    /*
     * Ustawiamy stan nazwy strony w bannerze
     */
    setBannerPageName(name) {
        this.setState((state) => ({
            banner: {
                name: name,
                additional: state.additional
            }
        }));
    }

    /*
     * Ustawiamy stan nazwy dodatkowej strony w banerze
     */
    setBannerPageAdditionalName(name) {
        this.setState((state) => ({
            banner: {
                name: state.name,
                additional: name
            }
        }));
    }

    /*
     * Header autoryzujacy uztkownika za pomoca access tokenu
     */
    createAuthorizationHeader() {
        const accessToken = localStorage.getItem('access_token');
        return {
            Authorization: `Bearer ${accessToken}`
        }
    }

    render() {
        return (
            <Router>
                <NavBar
                    logoutUser={this.logoutUser}
                    user={this.state.user}
                />
                <PageContent
                    loginUser={this.loginUser}
                    user={this.state.user}
                    setPageName={this.setBannerPageName}
                    setPageAdditionalName={this.setBannerPageAdditionalName}
                    banner={this.state.banner}
                />
            </Router>
        );
    }
}

export default App;
