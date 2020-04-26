import React from "react";
import {Switch, Route, withRouter} from 'react-router-dom';


import api from "../api";
import {CONFIG} from "../config";

import Spinner from "../components/spinner";
import Categories from "../components/categories";
import Threads from "../components/threads";

const initialState = {
    threadsData: []
};

class ForumThreads extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;
    }

    componentWillReceiveProps(nextProps) {
        const categoryId = this.props.match.params.categoryId;

        if (nextProps.match.params.categoryId !== categoryId) {
            this.setState((initialState));
            this.fetchThreadsByCategoryId(nextProps.match.params.categoryId)
                .then((response) => {
                    if (response.status === 200) {
                        this.setState({threadsData: response.data});
                    }
                })
        }
    }

    componentWillUnmount(): void {
        this.setState(initialState);
    }

    componentDidMount(): void {
        const categoryId = this.props.match.params.categoryId;
        this.fetchThreadsByCategoryId(categoryId)
            .then((response) => {
                if (response.status === 200) this.setState({threadsData: response.data});
            })
    }

    fetchThreadsByCategoryId(categoryId) {
        return api.get(CONFIG.API.ENDPOINTS.FORUM.THREADS, {params: {category: categoryId}})
    }

    render() {

        const categoriesData = this.props.categoriesData ? <Categories data={this.props.categoriesData}/> : <Spinner/>;

        const threadsData = this.state.threadsData ? <Threads data={this.state.threadsData} /> : <Spinner/>;

        return (
            <div className="row" style={{minHeight: '100vh'}}>
                <div className="col-md-1 offset-md-1 col-sm-12">
                    <ul className="nav flex-md-column">
                        {categoriesData}
                    </ul>
                </div>
                <div className="col-md-9 col-sm-12">
                    {threadsData}
                </div>
            </div>
        )
    }
}

export default withRouter(ForumThreads);