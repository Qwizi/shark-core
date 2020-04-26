import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faComments} from "@fortawesome/free-solid-svg-icons";
import {Animated} from "react-animated-css";

export default class ThreadDetailItem extends React.Component
{
    render() {
        const {data} = this.props;
        return (
            <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={true}>
                <div className="row">
                    <div className="col-md-10 offset-md-1">
                        <h2>{data.title}</h2>
                        <div className="card card-bg">
                            <div className="card-body">
                                <div className="row">
                                    <div className="col-md-2 text-center">
                                        <div className="row">
                                            <div className="col">
                                                <img className="img-fluid rounded-pill" src={data.author.avatarmedium}
                                                     alt={`${data.author.username}'s avatar`}/>
                                            </div>
                                        </div>
                                        <div className="row">
                                            <div className="col">
                                                {data.author.username}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-md-10" dangerouslySetInnerHTML={{__html: data.content}}/>
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
        )
    }
}