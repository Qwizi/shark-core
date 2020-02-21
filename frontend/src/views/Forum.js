import React from 'react';
import {Row, Col, Button, Card, ListGroup} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faStar} from '@fortawesome/free-solid-svg-icons';
import {Switch, Route, Redirect, withRouter} from 'react-router-dom';
import {
    Categories,
    Threads,
    PinnedThreads,
} from '../components/Forum';
import api from '../api';
import {Animated} from "react-animated-css";
import {
    Thread,
    NewThread
} from './';
import {CONFIG} from "../config";

const FORUM_THREADS_ENDPOINT = CONFIG.API.ENDPOINTS.FORUM.THREADS;

const ThreadRedirect = (props) => {
    if (props.new_thread_redirect) {
        return (
            <Redirect from={props.url} to={`${props.url}thread/new/`}/>
        )
    } else {
        return (
            <></>
        )
    }
};

class Forum extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            threads: [],
            threads_is_loaded: false,
            category_name: null,
            new_thread_redirect: false,
        };

        this.getThreads = this.getThreads.bind(this);
        this.setCategoryName = this.setCategoryName.bind(this)
        this.setThreadIsLoadedFalse = this.setThreadIsLoadedFalse.bind(this)
        this.clearThreads = this.clearThreads.bind(this)
        this.handleClickNewThreadButton = this.handleClickNewThreadButton.bind(this)
        this.setNewThreadRedirectFalse = this.setNewThreadRedirectFalse.bind(this)
    }

    componentDidMount() {
        this.props.setPageName('Forum');
        this.getThreads(null)
    }

    componentWillUnmount() {
        this.setState({
            new_thread_redirect: false,
            threads_is_loaded: false,
            threads: []
        })
    }

    getThreads(category_id) {
        if (category_id == null) {
            api.get(FORUM_THREADS_ENDPOINT)
                .then(response => {
                    const threads = response.data.results
                    this.setState({
                        threads: threads,
                        threads_is_loaded: true
                    })
                })
        } else {
            api.get(FORUM_THREADS_ENDPOINT + `?category=${category_id}`)
                .then(response => {
                    const threads = response.data.results
                    this.setState({
                        threads: threads,
                        threads_is_loaded: true
                    })
                })
        }
    }

    clearThreads() {
        this.setState({
            threads: []
        })
    }

    setCategoryName(category_name) {
        this.setState({
            category_name: category_name
        })
    }

    setThreadIsLoadedFalse() {
        this.setState({
            threads_is_loaded: false
        })
    }

    handleClickNewThreadButton() {
        this.setState({
            new_thread_redirect: true
        })
    }

    setNewThreadRedirectFalse() {
        this.setState({
            new_thread_redirect: false
        })
    }

    render() {
        const posts = ['test', '123', 'elo', '10', '5'];
        const {match} = this.props
        return (
            <div>
                <Switch>
                    <Route exact path={match.path}>
                        <ThreadRedirect
                            url={match.url}
                            new_thread_redirect={this.state.new_thread_redirect}
                        />
                        <Row>
                            <Col md={{span: 2, offset: 1}}>
                                <Card className="bonus-card">
                                    <Card.Body className="bonus-card-bg">
                                        <Card.Text>
                                            <Row>
                                                <Col>
                                                    <Button
                                                        variant="primary"
                                                        block
                                                        onClick={this.handleClickNewThreadButton}
                                                    >
                                                        Dodaj wątek
                                                    </Button>
                                                </Col>
                                            </Row>
                                            <Row>
                                                <Col md={{margin: 5}}>
                                                    <Categories
                                                        getThreads={this.getThreads}
                                                        setCategoryName={this.setCategoryName}
                                                        threads={this.state.threads}
                                                        setThreadIsLoadedFalse={this.setThreadIsLoadedFalse}
                                                        clearThreads={this.clearThreads}
                                                        {...this.props}
                                                    />
                                                </Col>
                                            </Row>
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                            <Col md={6}>
                                <Row>
                                    <Col md={{offset: 1}}>
                                        <p>Tematy </p>
                                    </Col>
                                </Row>
                                <Animated
                                    animationIn="fadeIn"
                                    isVisible={this.state.threads_is_loaded}
                                >
                                    <Threads
                                        getThreads={this.getThreads}
                                        setCategoryName={this.setCategoryName}
                                        category_name={this.state.category_name}
                                        threads={this.state.threads}
                                        {...this.props}
                                    />
                                </Animated>
                            </Col>
                            <Col md={{span: 2}}>
                                <Card className="bonus-card">
                                    <Card.Body className="bonus-card-bg">
                                        <Card.Title>Ostatnie tematy</Card.Title>
                                        <Card.Text>
                                            <ListGroup>
                                                {posts.map((post) =>
                                                    <ListGroup.Item className="bonus-card bonus-card-bg">{post}</ListGroup.Item>
                                                )}
                                            </ListGroup>
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </Route>
                    <Route path={`${match.url}/thread/new/`} {...this.props}>
                        <NewThread
                            setNewThreadRedirectFalse={this.setNewThreadRedirectFalse}
                            {...this.props}
                        />
                    </Route>
                    <Route path={`${match.url}/thread/:threadId/`} {...this.props}>
                        <Thread {...this.props} />
                    </Route>
                </Switch>
            </div>
        )
    }
}

export default withRouter(Forum)