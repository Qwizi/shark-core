import React from "react";
import {Switch, Route, withRouter} from 'react-router-dom';
import {ArticleCard} from "../components/acticle";
import {NewsDetail} from "./index";
import api from "../api";
import {CONFIG} from "../config";
import querystring from 'query-string';

const initialState = {
    newsData: []
};

class News extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;
    }

    componentDidMount(): void {
        this.fetchNews()
            .then((response) => {
                if (response.status === 200) this.setState({newsData: response.data})
            })
    }

    handleClickLoadMore() {
        //const updatedData = data.concat(data2);
        const {newsData} = this.state;

        if (newsData.next) {
            const splitUrl = newsData.next.split('/');
            const params = querystring.parse(splitUrl[splitUrl.length - 1]);

            console.log(params['page']);

            this.fetchNews({page: params['page']})
                .then((response) => {
                    if (response.status === 200) {
                        const newNewsResults =  response.data.results;
                        const newNewsNextUrl = response.data.next;

                        const updatedNewsResults = newsData.results.concat(newNewsResults);
                        this.setState({
                                newsData: {
                                    count: response.data.count,
                                    next: newNewsNextUrl,
                                    previous: newsData.next,
                                    results: updatedNewsResults},
                            }
                        );
                    }
                })
        }
        //this.setState({data: updatedData});
    }

    fetchNews(params = null) {
        const endpoint = CONFIG.API.ENDPOINTS.NEWS;

        return params == null ? api.get(endpoint) : api.get(endpoint, {params: params});
    }

    render() {
        const {match} = this.props;
        return (
            <Switch>
                <Route exact path={`${match.path}`}>
                    <ArticleCard data={this.state.newsData.results}/>
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
                <Route path={`${match.path}/:id`}>
                    <NewsDetail/>
                </Route>
            </Switch>
        )
    }
}

export default withRouter(News);
