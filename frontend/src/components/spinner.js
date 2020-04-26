import React from "react";


export default class Spinner extends React.Component
{
    render() {
        let center = '';

        if (this.props.center) {
            if (this.props.center === true) {
                center = 'justify-content-center';
            }
        }

        return (
            <div className={`d-flex ${center}`}>
                <div className="spinner-border text-secondary" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
            </div>
        )
    }
}

Spinner.defaultProps = {
    center: true
};