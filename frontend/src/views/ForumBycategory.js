import React from 'react';
import { Row, Col, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import { Switch, Route, Redirect, withRouter } from 'react-router-dom';

import { 
    Categories,
    Threads,
    PinnedThreads
} from '../components/Forum';

class ForumByCategory extends React.Component
{
    componentDidMount() {
        this.props.setPageName('ForumByCategory')
        console.log(this.props.match.url)
    }

    render() {
        const { location, match } = this.props
        const { path } = location.pathname
        return (
            <div>
                <Switch>
                    <Route exact path={match.url}>
                       123
                    </Route>
                </Switch>
            </div>
        )
    }
}

export default withRouter(ForumByCategory)