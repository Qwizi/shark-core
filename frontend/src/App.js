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
                id: null,
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
        const {logged} = user;
        console.log(logged);
        if (user.logged) {
            console.log(localStorage.getItem('access_token'));
            console.log(user.logged);
            this.getUserData().then(userData => {
                this.setUserState(userData);
            })
        }
    }


    /*
    async componentDidMount() {
        const {logged} = this.state.user
        if (logged) {

            const refresh_token = localStorage.getItem('refresh_token')
            this.getUserData()
                .then(user => {
                    this.setState((state) => ({
                        user: {logged: state.user.logged, ...user}
                    }))
                })
                .catch(error => {
                    if (error.response.status === 401) {
                        this.getNewToken(refresh_token)
                            .then(new_token => {
                                localStorage.setItem('access_token', new_token)
                                this.getUserData()
                                    .then(user => {
                                        this.setState((state) => ({
                                            user: {logged: state.user.logged, ...user}
                                        }))
                                    })
                            })
                            .catch(error => {
                                if (error.response.status === 401) {
                                    this.logOutUser()
                                }
                            })

                    }
                })

            // const user = this.getUserData()
            //this.setState((state) => ({
            //user: {logged: state.user.logged, ...user}
            //}))
        }
    }*/

    /*
     * Logujemy uzytkownika
     */
    loginUser = async (params) => {
        // Pobieramy tokeny z api
        this.getAuthTokens(params).then(data => {
            localStorage.setItem('access_token', data.access);
            console.log(localStorage.getItem('access_token'));
            //Pobieramy dane zalogowanego uzytkownika
            this.getUserData().then(userData => {
                console.log(userData);
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
        localStorage.removeItem('access_token');
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
    setUserState(userData, logged=null) {
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
                id: null,
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
                />
            </Router>
        );
    }
}

export default App;
