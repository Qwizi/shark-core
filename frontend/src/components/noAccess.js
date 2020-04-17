import React from "react";

export default class NoAccess extends React.Component {
    render() {
        const {httpError} = this.props;
        return (
            <div className="row">
                <div className="col">
                    <div className="card card-bg">
                        <div className="card-header">
                            {httpError.detail}
                        </div>
                        <div className="card-body">
                           Nie posiadasz odpowiednich uprawnien do wyswietlania tej strony.
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}