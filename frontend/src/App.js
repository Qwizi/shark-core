import React from 'react';
import './App.css';
import {Switch, Route, BrowserRouter, Redirect} from 'react-router-dom';

import {Navbar} from './components/navbar';
import {Footer} from "./components/footer";

import {
    News,
    NewsDetail,
    Forum,
    SteamCallback,
    SteamLoginRedirect
} from './views';

import {tokenStorage} from "./TokenStorage";
import {CONFIG} from "./config";
import api from "./api";

const initialState = {
    logged: false,
    user: {}
};

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;

        this.loginUser = this.loginUser.bind(this);
        this.logoutUser = this.logoutUser.bind(this);
    };

    async componentDidMount(): void {
        // Jezeli nie istnieje access token w localStorage nic nie robimy
        if (!tokenStorage.getAccessToken()) return;


        // Pobieramy dane dla zalogowanego uzytkownika
        api.get(CONFIG.API.ENDPOINTS.ACCOUNTS.ME)
            .then((response) => {
                // Jezeli zworocono status 200 ustawiamy stan zalogowanego uzytkownika
                if (response.status === 200) this.setUserLoggedState(response.data);
            })
            .catch((error) => {
                if (error.response) {
                    // Jezeli zwrocono status 401 wykorzystujemy do zapytania refresh token
                    if (error.response.status === 401) {
                        // Pobieramy refresh token z localStorage
                        const refreshToken = tokenStorage.getRefreshToken();

                        // Jezeli nie istnieje wylogowujemy uzytkownika
                        if (!refreshToken) this.logoutUser();

                        // Robimy zapytanie po nowy acccess token przekazujac refresh token
                        api.post(CONFIG.API.ENDPOINTS.TOKEN.REFRESH, {
                            refresh: refreshToken
                        })
                            .then((response) => {
                                // Jezeli zwrocono status 200 ustawiamy nowy access token
                                if (response.status === 200) {
                                    // ustawiamy nowy access token
                                    tokenStorage.setAccessToken(response.data.access);
                                    // Usuwamy refresh token z localStorage
                                    tokenStorage.removeRefreshToken();

                                    // Ponownie robimy zapytanie, ktore pobiera dane zalogowanego uzytkonwika. Tylko tym razem wykorzystujemy nowy token
                                    api.get(CONFIG.API.ENDPOINTS.ACCOUNTS.ME, {
                                        headers: {
                                            'Authorization': `Bearer ${response.data.access}`
                                        }
                                    })
                                        .then((response) => {
                                            // Jezeli wzrocono status 200 ustawiamy stan zalogowanego uzytkownika
                                            if (response.status === 200) this.setUserLoggedState(response.data);
                                        })
                                        .catch((error) => {
                                            if (error.response) {
                                                // Jezeli zwrocno blad ze statusem 401 wylogowujemy uzytkownika
                                                if (error.response.status === 401) this.logoutUser();
                                            }
                                        })
                                }
                            })
                            .catch((error) => {
                                if (error.response) {
                                    // Jezeli zwrocno blad ze statusem 401 wylogowujemy uzytkownika
                                    if (error.response.status === 401) this.logoutUser();
                                }
                            })
                    }
                }
            });

        /*const response = await api.get(CONFIG.API.ENDPOINTS.ACCOUNTS.ME);

        if (response.status === 200) this.setState({logged: true, user: response.data});

        else if (response.status === 401) {
            console.log('Token wygasl')

            const refreshToken = tokenStorage.getRefreshToken();

            const refreshTokenResponse = await this.getAccessTokenByRefreshToken(refreshToken);

            if (refreshTokenResponse.status === 200) {
                tokenStorage.setAccessToken(refreshTokenResponse.data);
                tokenStorage.removeRefreshToken();

                const secondResponse = await this.getUserMeResponse();

                if (secondResponse.status === 200) {
                    this.setState({logged: true, user: secondResponse.data})
                } else {
                    this.logoutUser();
                }
            }
        }*/
    };

    // Pobieramy dane zalogowanego uzytkownika
    async getUserMeResponse() {
        try {
            return await api.get(CONFIG.API.ENDPOINTS.ACCOUNTS.ME);
        } catch (error) {
            console.log(error);
        }
    }

    // Pobieramy tokeny
    async getTokensResponse(params) {
        try {
            return await api.post(CONFIG.API.ENDPOINTS.TOKEN.AUTH, params);
        } catch (error) {
            console.log(error)
        }
    }

    async getAccessTokenByRefreshToken(accessToken) {
        try {
            return await api.post(CONFIG.API.ENDPOINTS.TOKEN.REFRESH, accessToken)
        } catch (error) {
            console.log(error);
        }
    }

    // Logujemy uzytkownika
    async loginUser(params) {
        // pobieramy tokeny
        const tokensResponse = await this.getTokensResponse(params);

        // Jezeli tokeny zostaly pobrane ustawiamy je localStorage
        if (tokensResponse.data) await tokenStorage.setTokens(tokensResponse.data.access, tokensResponse.data.refresh);

        // Jezli tokeny zostaly ustawione w localStorage pobieramy dane uzytkownika
        if (tokenStorage.getAccessToken() && tokenStorage.getRefreshToken()) {

            const response = await api.get(CONFIG.API.ENDPOINTS.ACCOUNTS.ME, {
                headers: {
                    'Authorization': `Bearer ${tokensResponse.data.access}`
                }
            });

            this.setState({logged: true, user: response.data});
        }
    }

    logoutUser() {
        // Resetujemy stan i usuwamy tokeny
        this.setState(initialState);
        tokenStorage.removeTokens();
    }

    setUserLoggedState(userData) {
        this.setState({logged: true, user: userData});
    }

    render() {
        const steamCallbackEndpoint = CONFIG.STEAM.CALLBACK || '/auth/steam/callback/';
        const steamRedirectEndpoint = CONFIG.STEAM.REDIRECT || '/auth/steam/redirect/';
        return (
            <BrowserRouter>
                <Navbar
                    logged={this.state.logged}
                    logout={() => this.logoutUser}
                    user={this.state.user}
                />
                <main className="container-fluid wrapper">
                    <Switch>
                        <Route
                            exact strict path="/:url*"
                            render={props => <Redirect to={`${props.location.pathname}/`}/>}
                        />

                        <Route exact path="/" render={() => <News/>}/>
                        <Route exact path="/news/" render={() => <News/>}/>
                        <Route path="/news/:id/" render={(props) => <NewsDetail {...props}/>}/>
                        <Route exact path="/forum/" render={() => <Forum/>}/>
                        <Route exact path={`${steamCallbackEndpoint}`}>
                            <SteamCallback
                                login={this.loginUser}
                            />
                        </Route>
                        <Route exact path={`${steamRedirectEndpoint}`} render={() => <SteamLoginRedirect/>}/>
                    </Switch>
                </main>
                <Footer/>
            </BrowserRouter>
        );
    }
}

export default App;
