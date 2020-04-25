import React from 'react';
import './App.css';
import {Switch, Route, BrowserRouter, Redirect} from 'react-router-dom';

import {Navbar} from './components/navbar';
import {Footer} from "./components/footer";
import NoAccess from './components/noAccess';

import Routes from "./routes";

import {tokenStorage} from "./TokenStorage";
import {CONFIG} from "./config";
import api from "./api";
import ERROR_CODES from "./errorCodes";

const userInitialState = {
    logged: false,
    user: {
        username: "Guest"
    }
};

const initialState = {
    ...userInitialState,
    httpError: {show: false, detail: ''},
};

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;

        this.loginUser = this.loginUser.bind(this);
        this.logoutUser = this.logoutUser.bind(this);
    };

    componentDidMount() {
        // Jezeli nie istnieje access token w localStorage nic nie robimy
        if (!tokenStorage.getAccessToken()) return;

        this.getUserMeData();
    };

    fetchUserMeData(forceAuthToken = null) {
        if (forceAuthToken) return api.get(CONFIG.API.ENDPOINTS.ACCOUNTS.ME, {
            headers: {
                'Authorization': `Bearer ${forceAuthToken}`
            }

        });
        return api.get(CONFIG.API.ENDPOINTS.ACCOUNTS.ME);
    }

    fetchTokens(params) {
        return api.post(CONFIG.API.ENDPOINTS.TOKEN.AUTH, params);
    }

    fetchAccessTokenByRefreshToken(refreshToken) {
        return api.post(CONFIG.API.ENDPOINTS.TOKEN.REFRESH, {refresh: refreshToken});
    }

    setUserLoggedState(userData) {
        this.setState({logged: true, user: userData});
    }

    // Logujemy uzytkownika
    loginUser(params) {
        this.fetchTokens(params)
            .then((response) => {
                if (response.status === 200) {
                    const tokens = response.data;

                    tokenStorage.setTokens(tokens.access, tokens.refresh);

                    const accessToken = tokenStorage.getAccessToken();
                    const refreshToken = tokenStorage.getRefreshToken();

                    if (accessToken && refreshToken) {
                        this.fetchUserMeData(accessToken).then((response) => {
                            if (response.status === 200) this.setUserLoggedState(response.data);
                        })
                            .catch((error) => {
                                if (error.response) {
                                    if (error.response.status === 401) console.log(ERROR_CODES.E001);
                                }
                            })
                    }

                }
            })
    }

    logoutUser() {
        // Resetujemy stan i usuwamy tokeny
        this.setState(userInitialState);
        tokenStorage.removeTokens();
    }

    getUserMeData() {
        // Pobieramy dane dla zalogowanego uzytkownika
        this.fetchUserMeData()
            .then((response) => {
                // Jezeli zworocono status 200 ustawiamy stan zalogowanego uzytkownika
                if (response.status === 200) this.setUserLoggedState(response.data);
            })
            .catch((error) => {
                if (error.response) {
                    // Jezeli zwrocono status 401 wykorzystujemy do zapytania refresh token
                    if (error.response.status === 401) {
                        console.log(ERROR_CODES.E002);
                        // Pobieramy refresh token z localStorage
                        const refreshToken = tokenStorage.getRefreshToken();

                        // Jezeli nie istnieje wylogowujemy uzytkownika
                        if (!refreshToken) this.logoutUser();

                        // Robimy zapytanie po nowy acccess token przekazujac refresh token
                        this.fetchAccessTokenByRefreshToken(refreshToken)
                            .then((response) => {
                                // Jezeli zwrocono status 200 ustawiamy nowy access token
                                if (response.status === 200) {
                                    // ustawiamy nowy access token
                                    tokenStorage.setAccessToken(response.data.access);
                                    // Usuwamy refresh token z localStorage
                                    tokenStorage.removeRefreshToken();

                                    // Ponownie robimy zapytanie, ktore pobiera dane zalogowanego uzytkonwika. Tylko tym razem wykorzystujemy nowy token
                                    this.fetchUserMeData(response.data.access)
                                        .then((response) => {
                                            // Jezeli wzrocono status 200 ustawiamy stan zalogowanego uzytkownika
                                            if (response.status === 200) this.setUserLoggedState(response.data);
                                        })
                                        .catch((error) => {
                                            if (error.response) {
                                                // Jezeli zwrocno blad ze statusem 401 wylogowujemy uzytkownika
                                                if (error.response.status === 401) {
                                                    this.logoutUser();
                                                    console.log(ERROR_CODES.E004)
                                                }
                                            }
                                        })
                                }
                            })
                            .catch((error) => {
                                if (error.response) {
                                    // Jezeli zwrocno blad ze statusem 401 wylogowujemy uzytkownika
                                    if (error.response.status === 401) {
                                        this.logoutUser();
                                        console.log(ERROR_CODES.E003);
                                    }
                                }
                            })
                    }
                }
            });
    }

    render() {
        return (
            <BrowserRouter>
                <Navbar
                    logged={this.state.logged}
                    logout={() => this.logoutUser}
                    user={this.state.user}
                />
                <main className="container-fluid wrapper">
                    <Routes
                        logged={this.state.logged}
                        user={this.state.user}
                        login={this.loginUser}
                    />
                </main>
                <Footer/>
            </BrowserRouter>
        );
    }
}

export default App;
