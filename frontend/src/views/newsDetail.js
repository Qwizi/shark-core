import React from "react";
import PropTypes from 'prop-types';
import {Animated} from "react-animated-css";
import api from "../api";
import {CONFIG} from "../config";
import {withRouter} from "react-router-dom";

const initialData = {
    newsData: {}
};

class NewsDetail extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialData;
    }

    componentDidMount(): void {
        const newsId = this.props.match.params.id;
        this.fetchNewsById(newsId)
            .then((response) => {
                if (response.status === 200) {
                    this.setState({newsData: response.data});
                }
            })
    }

    fetchNewsById(newsId) {
        const endpoint = CONFIG.API.ENDPOINTS.NEWS;
        return api.get(endpoint+newsId);
    }

    render() {
        const {newsData} = this.state;
        return (
            <>
                {<div className="row">
                    <div className="col">
                        <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={true}>
                            <div className="jumbotron jumbotron-fluid jumbotron-bg" >
                                <div className="container-fluid">
                                    <h1 className="display-6">
                                        {newsData.title}
                                    </h1>
                                    <p className="lead">
                                        {newsData.content}
                                    </p>
                                </div>
                            </div>
                        </Animated>
                    </div>
                </div>
                }
            </>
        )
    }
}

export default withRouter(NewsDetail)
