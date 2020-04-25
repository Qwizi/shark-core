import React from "react";
import {Animated} from "react-animated-css";
import {Link} from "react-router-dom";
import Spinner from "./spinner";


export default class ArticleItem extends React.Component
{
    render() {
        const {article} = this.props;

        if (!article) return <Spinner />

        return (
            <div className="row">
                <div className="col">
                    <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={true}>
                        <div className="jumbotron jumbotron-fluid jumbotron-bg">
                            <div className="container-fluid">
                                <h1 className="display-6">
                                    <Link to={`/news/${article.id}/${article.slug}/`}>{article.title}</Link>
                                </h1>
                                <p className="lead">{article.content}</p>
                            </div>
                        </div>
                    </Animated>
                </div>
            </div>
        )
    }
}

ArticleItem.defaultProps = {
    article: {}
};