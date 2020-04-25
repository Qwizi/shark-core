import React from "react";
import PropTypes from 'prop-types';

export default class Alert extends React.Component {
    render() {
        const {type, content} = this.props;
        return (
            <div className={`alert alert-${type}`} role="alert">
                {content}
            </div>
        )
    }
}

Alert.defaultProps = {
    type: 'danger',
    content: 'Danger alert!'
};

Alert.propTypes = {
    type: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired
};