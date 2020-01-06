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

class Forum extends React.Component
{
    componentDidMount() {
        this.props.setPageName('Forum')
    }

    render() {
        const { location, match } = this.props
        const { path } = location.pathname
        return (
            <div>
                <Switch>
                    <Route exact path={match.path}>
                        <Row>
                            <Col md={{ span: 3, offset: 1 }}><Button variant="primary" block>Dodaj wątek</Button></Col>
                            <Col md={7}>
                                <Row>
                                    <Col md={{span: 6, offset: 1}}>
                                        <p>Przypięte tematy <FontAwesomeIcon icon={faStar} /></p>
                                    </Col>
                                </Row>
                                <Row>
                                    <Col md={{ offset: 1 }}>
                                        <Row>
                                            <PinnedThreads />
                                        </Row>
                                    </Col>
                                </Row>
                            </Col>
                        </Row>
                        <Row>
                            <Col md={{ span: 3, offset: 1 }}>
                                <p>Kategorie</p>
                                <Categories />
                            </Col>
                            <Col md={7}>
                                <Row>
                                    <Col md={{ offset: 1 }}>
                                    <p>Najnowsze tematy </p>
                                    </Col>
                                </Row>
                                <Threads />
                            </Col>d
                        </Row>
                    </Route>
                    <Route path={`${match.url}/:id/`} render={({match}) =>( <div> <h3> {match.params.id}</h3></div>)}/>
                </Switch>
            </div>
        )
    }
}

export default withRouter(Forum)