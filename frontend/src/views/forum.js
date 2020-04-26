import React from "react";
import {Switch, Route, withRouter} from 'react-router-dom';
import axios from 'axios';

import api from "../api";
import {CONFIG} from "../config";


import Spinner from "../components/spinner";
import Threads from "../components/threads";

import ForumThreads from "./forumThreads";
import Categories from "../components/categories";
import ForumThreadDetail from "./forumThreadDetail";

const initialState = {
    categoriesData: [],
    lastThreadsData: []
};

class Forum extends React.Component {

    constructor(props) {
        super(props);

        this.state = initialState;
    }

    componentDidMount(): void {
        axios.all([this.fetchCategories(), this.fetchLastThreads()])
            .then(axios.spread((categoriesRes, lastThreadsRes) => {
                if (categoriesRes.status === 200) this.setState({categoriesData: categoriesRes.data});
                if (lastThreadsRes.status === 200) this.setState({lastThreadsData: lastThreadsRes.data});
            }));
    }

    fetchCategories() {
        return api.get(CONFIG.API.ENDPOINTS.FORUM.CATEGORIES);
    }

    fetchLastThreads() {
        return api.get(CONFIG.API.ENDPOINTS.FORUM.THREADS);
    }

    render() {
        const {match} = this.props;

        const categoriesData = this.state.categoriesData ? <Categories data={this.state.categoriesData}/> : <Spinner/>;
        const lastThreadsData = this.state.lastThreadsData ? <Threads data={this.state.lastThreadsData}/> : <Spinner />;

        return (
            <Switch>
                <Route exact path={`${match.path}`}>
                    <div className="row" style={{minHeight: '100vh'}}>
                        <div className="col-lg-1 offset-lg-1 col-sm-12">
                            <ul className="nav flex-md-column">
                                {categoriesData}
                            </ul>
                        </div>
                        <div className="col-md-9 col-sm-12">
                            {lastThreadsData}
                        </div>
                    </div>
                </Route>
                <Route path={`${match.path}/category/:categoryId/`}>
                    <ForumThreads timestamp={new Date().toString()} categoriesData={this.state.categoriesData}/>
                </Route>
                <Route path={`${match.path}/thread/:threadId/`}>
                    <ForumThreadDetail user={this.props.user}/>
                </Route>
            </Switch>
        )
    }
}


export default withRouter(Forum);
