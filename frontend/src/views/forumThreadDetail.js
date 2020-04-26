import React from "react";
import {Link, withRouter} from 'react-router-dom';


import api from "../api";
import {CONFIG} from "../config";
import axios from 'axios';

import Spinner from "../components/spinner";
import ThreadDetailItem from "../components/threadDetailItem";
import Posts from "../components/posts";

const initialState = {
    threadData: {},
    postsData: {}
};

class ForumThreadDetail extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;

        this.updatePostsData = this.updatePostsData.bind(this);
    }

    componentDidMount(): void {
        const threadId = this.props.match.params.threadId;

        axios.all([this.fetchThreadById(threadId), this.fetchThreadPosts(threadId)])
            .then(axios.spread((threadRes, postsRes) => {
                if (threadRes.status === 200) this.setState({threadData: threadRes.data});
                if (postsRes.status === 200) this.setState({postsData: postsRes.data});
            }))
    }

    fetchThreadById(threadId) {
        return api.get(CONFIG.API.ENDPOINTS.FORUM.THREADS + threadId);
    }

    fetchThreadPosts(threadId) {
        return api.get(CONFIG.API.ENDPOINTS.FORUM.POSTS, {params: {thread: threadId}});
    }

    updatePostsData(newPostData) {
        const oldData = this.state.postsData.results;
        const newData = oldData.concat(newPostData);

        this.setState({postsData: {results: newData}});
    }

    render() {
        const {threadData, postsData} = this.state;

        if (!threadData || !threadData.title) return <Spinner/>;


        return (
            <>
                <ThreadDetailItem data={threadData} />
                <Posts
                    threadId={threadData.id}
                    authorId={this.props.user.id}
                    data={postsData}
                    updatePostsData={this.updatePostsData}
                />
            </>
        );
    }
}

export default withRouter(ForumThreadDetail)