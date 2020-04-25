import React from "react";
import {Switch, Route, withRouter} from 'react-router-dom';
import {ArticleCard} from "../components/acticle";
import {NewsDetail} from "./index";
import api from "../api";
import {CONFIG} from "../config";
import querystring from 'query-string';
import Spinner from "../components/spinner";
import Articles from "../components/articles";

const initialState = {
    newsData: [],
};

class News extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;
    }

    componentWillUnmount(): void {
        this.setState(initialState);
    }

    componentDidMount(): void {
        this.fetchNews()
            .then((response) => {
                if (response.status === 200) {
                    this.setState({newsData: response.data});
                }
            })
    }

    handleClickLoadMore() {
        const {newsData} = this.state;

        if (newsData.next) {
            const splitUrl = newsData.next.split('/');
            const params = querystring.parse(splitUrl[splitUrl.length - 1]);

            console.log(params['page']);

            this.fetchNews({page: params['page']})
                .then((response) => {
                    if (response.status === 200) {
                        const newNewsResults = response.data.results;
                        const newNewsNextUrl = response.data.next;

                        const updatedNewsResults = newsData.results.concat(newNewsResults);
                        this.setState({
                                newsData: {
                                    count: response.data.count,
                                    next: newNewsNextUrl,
                                    previous: newsData.next,
                                    results: updatedNewsResults
                                },
                            }
                        );
                    }
                })
        }
    }

    fetchNews(params = null) {
        const endpoint = CONFIG.API.ENDPOINTS.NEWS;

        return params == null ? api.get(endpoint) : api.get(endpoint, {params: params});
    }

    render() {
        const {match} = this.props;

        const newsData = this.state.newsData ? <Articles data={this.state.newsData}/> : <Spinner />;

        return (
            <Switch>
                <Route exact path={`${match.path}`}>
                    {newsData}
                    <div className="row">
                        <div className="col text-center">
                            {this.state.newsData.next && (
                                <button
                                    className="btn btn-success btn-lg btn-block"
                                    onClick={() => this.handleClickLoadMore()}
                                >
                                    Show more
                                </button>
                            )
                            }
                        </div>
                    </div>
                </Route>
                <Route path={`${match.path}/:id/:slug/`}>
                    <NewsDetail/>
                </Route>
            </Switch>
        )
    }
}

export default withRouter(News);
