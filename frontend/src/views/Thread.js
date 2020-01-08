import React from 'react';
import { Row, Col, Button, Card, Badge } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import { Link as RouterLink, Switch, Route, Redirect, withRouter } from 'react-router-dom';
import { Link, DirectLink, Element, Events, animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'
import api from '../api';
import { Animated } from "react-animated-css";

class Thread extends React.Component
{

    constructor(props) {
        super(props)

        this.state = {
            thread: {},
            author: {},
            posts: []
        }
    }

    componentDidMount() {
        Events.scrollEvent.register('begin', function() {
            console.log("begin", arguments);
        })

        Events.scrollEvent.register('end', function () {
            console.log("end", arguments);
        })
        scroller.scrollTo('thread-content', {
          duration: 800,
          delay: 0,
          smooth: 'easeInOutQuart'
        })
        const params = this.props.match.params
        console.log(params.threadId)
        api.get(`/forum/threads/${params.threadId}/`)
            .then(response => {
                const thread = response.data
                this.setState({
                    thread: thread, 
                    author: thread.author
                })
                console.log(thread)
            })

        api.get(`/forum/posts/?thread=${params.threadId}`)
            .then(response => {
                const posts = response.data.results
                this.setState({
                    posts: posts
                })
                console.log(posts)
            })
    }

    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
    }

    scrollTo() {
        scroller.scrollTo('thread-content', {
          duration: 800,
          delay: 0,
          smooth: 'easeInOutQuart'
        })
      }

    render() {
        const { thread, author, posts } = this.state
        return (
            <div id="thread-content">

                <Animated 
                    animationIn="fadeIn" 
                    isVisible={true}
                >
                <Row>
                    <Col md={{span: 8, offset: 2}}>
                        <h2>{thread.title}</h2>
                        <Card key={thread.id} className="bonus-card">
                            <Card.Body className="bonus-card-bg">
                                <Card.Title>{author.username}</Card.Title>
                                <Card.Text>
                                    {thread.content}
                                </Card.Text>
                            </Card.Body> 
                        </Card>
                    </Col> 
                </Row>
                <Row>
                    <Col md={{span: 8, offset: 2}}>
                    <h3>Odpowiedzi: </h3>
                    </Col>
                    {posts.map((post) =>
                        <Col md={{span: 8, offset: 2}}>
                            <Card key={post.id} className="bonus-card">
                                <Card.Body className="bonus-card-bg">
                                    <Card.Title>...</Card.Title>
                                    <Card.Text>
                                        {post.content}
                                    </Card.Text>
                                </Card.Body> 
                            </Card>
                        </Col> 
                    )}
                </Row>
                </Animated>
            </div>
        )
    }
}

export default withRouter(Thread)