import React from "react";
import Spinner from "./spinner";
import PostItem from "./postItem";
import NewPost from "./newPost";

export default class Posts extends React.Component
{
    render() {
        const {data, threadId, authorId} = this.props;

        if (!data || !data.results) return <Spinner />;
        if (!data.results.length) return (
            <NewPost
                threadId={threadId}
                authorId={authorId}
                updatePostsData={this.props.updatePostsData}
            />
        );

        return (
            <>
                {data.results.map((post) =>
                    <PostItem
                        content={post.content}
                        author={post.author}
                    />
                )}
                <NewPost
                    threadId={threadId}
                    authorId={authorId}
                    updatePostsData={this.props.updatePostsData}
                />
            </>
        )
    }
}