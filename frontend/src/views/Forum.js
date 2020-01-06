import React from 'react';
import { Row, Col, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import { Switch, Route, Redirect, withRouter } from 'react-router-dom';
import { 
    Categories,
    Threads,
    PinnedThreads,
    LastThreads
} from '../components/Forum';
import api from '../api';
import { Animated } from "react-animated-css";

class Forum extends React.Component
{

    constructor(props) {
        super(props)

        this.state = {
            threads: [],
            threads_is_loaded: false,
            category_name: null
        }

        this.getThreads = this.getThreads.bind(this)
        this.setCategoryName = this.setCategoryName.bind(this)
        this.setThreadIsLoadedFalse = this.setThreadIsLoadedFalse.bind(this)
        this.clearThreads = this.clearThreads.bind(this)
    }

    getThreads(category_id) {
        if (category_id == null) {
            api.get(`/forum/threads/`)
            .then(response => {
                const threads = response.data.results
                this.setState({
                    threads: threads,
                    threads_is_loaded: true
                })
            })
        } else {
            api.get(`/forum/threads/?categories=${category_id}`)
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

    componentDidMount() {
        this.props.setPageName('Forum')
        this.getThreads(null)
    }

    render() {
        const { match } = this.props
        return (
            <div>
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
                                
                                    <Animated 
                                        animationIn="fadeIn"  
                                        isVisible={this.state.threads_is_loaded}
                                    >
                                    <Row>
                                    
                                    <PinnedThreads />
                                    </Row>
                                    </Animated>
                                
                            </Col>
                        </Row>
                    </Col>
                </Row>
                <Row>
                    <Col md={{ span: 3, offset: 1 }}>
                        <p>Kategorie</p>
                        <Categories 
                            getThreads={this.getThreads}
                            setCategoryName={this.setCategoryName}
                            threads={this.state.threads}
                            setThreadIsLoadedFalse={this.setThreadIsLoadedFalse}
                            clearThreads={this.clearThreads} 
                            {...this.props}
                        />
                    </Col>
                    <Col md={7}>
                        <Switch>
                            <Route exact path={match.path}>
                                <Row>
                                    <Col md={{ offset: 1 }}>
                                        <p>Najnowsze tematy </p>
                                    </Col>
                                </Row>
                                <Animated 
                                    animationIn="fadeIn" 
                                    isVisible={this.state.threads_is_loaded}
                                >
                                    <LastThreads 
                                        getThreads={this.getThreads} 
                                        threads={this.state.threads} 
                                        {...this.props}
                                    />
                                </Animated>
                            </Route>
                            <Route exact path={`${match.url}/threads`}>
                                <Row>
                                    <Col md={{ offset: 1 }}>
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
                            </Route>
                        </Switch>
                    </Col>
                </Row>
            </div>
        )
    }
}

export default withRouter(Forum)