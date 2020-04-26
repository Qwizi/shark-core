import React from "react";
import {Animated} from "react-animated-css";

export default class PostItem extends React.Component
{
    render() {
        const {content, author} = this.props;

        return (
            <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={!!content}>
                <div className="row">
                    <div className="col-md-10 offset-md-1">
                        <div className="card card-bg">
                            <div className="card-body">
                                <div className="row">
                                    <div className="col-md-2 text-center">
                                        <div className="row">
                                            <div className="col">
                                                <img className="img-fluid rounded-pill" src={author.avatarmedium}
                                                     alt={`${author.username}'s avatar`}/>
                                            </div>
                                        </div>
                                        <div className="row">
                                            <div className="col">
                                                {author.username}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-md-10" dangerouslySetInnerHTML={{__html: content}}/>
                                </div>
                                <div className="row">
                                    <div className="col-md-3 offset-md-10">
                                        <button className="btn btn-secondary btn-sm">Dodaj reakcje</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </Animated>
        );
    }
}

PostItem.defaultProps = {
    title: '',
    content: '',
    author: {}
};