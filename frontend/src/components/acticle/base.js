import React from "react";
import PropTypes from 'prop-types';
import {Link} from "react-router-dom";
import {Animated} from "react-animated-css";

export default class ArticleCard extends React.Component {

    substringContent(content, maxlength= 800) {
        return content.substring(0, maxlength) + '...';
    }

    render() {
        const {data} = this.props;

        const formattedData = [];

        data.map((data) => {
            if (data.content.length > 800) {
                data.content = this.substringContent(data.content);
            }

            if (data.title.length > 40) {
                data.title = this.substringContent(data.title, 40);
            }

            formattedData.push(data);

        });

        return (
            <>
                {formattedData.map((article) =>
                    <div className="row">
                        <div className="col">
                            <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={true}>
                                <div className="jumbotron jumbotron-fluid jumbotron-bg">
                                    <div className="container-fluid">
                                        <h1 className="display-6">
                                            <Link to={`/news/${article.id}/`}>{article.title}</Link>
                                        </h1>
                                        <p className="lead">{article.content}</p>
                                    </div>
                                </div>
                            </Animated>
                        </div>
                    </div>
                )}
            </>
        )
    }
}

ArticleCard.propTypes = {
    data: PropTypes.array.isRequired
};