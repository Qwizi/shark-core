import React from "react";
import PropTypes from 'prop-types';
import {Animated} from "react-animated-css";

export default class ThreadItem extends React.Component {
    render() {
        const {title, content} = this.props;
        return (
            <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={!!title}>
                <div className="card card-bg">
                    <div className="card-body">
                        <div className="card-title">{title}</div>
                        <div className="card-text" dangerouslySetInnerHTML={{__html: content}}>
                        </div>
                    </div>
                </div>
            </Animated>
        )
    }
}

ThreadItem.defaultProps = {
    title: '',
    content: ''
};

ThreadItem.propTypes = {
    title: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired
};

