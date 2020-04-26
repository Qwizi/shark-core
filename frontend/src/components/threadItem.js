import React from "react";
import PropTypes from 'prop-types';
import {Animated} from "react-animated-css";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faComments} from "@fortawesome/free-solid-svg-icons";

export default class ThreadItem extends React.Component {
    render() {
        const {
            id,
            title,
            content,
            username,
            avatar,
            created,
            posts,
            reactions,
            lastposter
        } = this.props;

        return (
            <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={!!title}>
                <div id={`thread-${id}`} className="card card-bg">
                    <div className="card-header">
                        <Link to={`/forum/thread/${id}/`}>{title}</Link>
                    </div>
                    <div className="card-body">
                        <div className="row">
                            <div className="col-md-1">
                                <div className="text-center">
                                    <img className="img-fluid rounded-pill" src={avatar} alt={`${username}'s avatar`}/>
                                </div>
                            </div>
                            <div className="col-md-10" dangerouslySetInnerHTML={{__html: content}}/>
                            <div className="col-md-1">
                                <div className="text-center">
                                    {lastposter && lastposter.avatar ? (
                                        <img className="img-fluid rounded-pill" src={lastposter.avatar}
                                             alt={`${lastposter.username}'s avatar`}/>
                                    ) : (
                                        <img className="img-fluid rounded-pill" src={avatar}
                                             alt={`${username}'s avatar`}/>
                                    )}
                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-md-1 text-center">
                                {username}
                            </div>
                            <div className="col-md-1 offset-md-10">
                                <div className="text-center">
                                    {lastposter && lastposter.username ? (<>{lastposter.username}</>) : <>{username}</>}
                                </div>
                            </div>
                        </div>
                    </div>
                    <footer className="card-footer">
                        <FontAwesomeIcon icon={faComments}/> {posts}
                    </footer>
                </div>
            </Animated>
        )
    }
}

ThreadItem.defaultProps = {
    id: 0,
    title: '',
    content: '',
    username: '',
    avatar: '',
    created: '',
    posts: 0,
    reactions: 0,
    lastposter: null,
};

ThreadItem.propTypes = {
    title: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired
};

