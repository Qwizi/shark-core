import React from 'react';
import { Row, Col, Card, Button, Form } from 'react-bootstrap';
import { withRouter } from 'react-router-dom';
import { Events, scroller } from 'react-scroll'
import api from '../api';
import { Animated } from "react-animated-css";
import EditorJs from "react-editor-js";
import { EDITOR_JS_TOOLS } from '../components/Forum/tools';
import CKEditor from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import Parser from 'html-react-parser';

const NewPostForm = (props) => {
        let display = 'none'

        if (props.post_display) {
            display = 'block'
        }

        return (
            <div id="new-post">
                <Animated 
                    animationIn="fadeInUp"
                    animationOut="fadeOutDown"
                    isVisible={props.show_new_post_form}
                    animateOnMount={false}
                >
                <Row style={{display: display}}>
                    <Col md={{span: 8, offset: 2}}>
                        <Card className="bonus-card">
                            <Card.Body className="bonus-card-bg">
                                <Card.Title>Odpowiedz</Card.Title>
                                <Card.Text>
                                    <Form>
                                        <Form.Group as={Row} controlId="formPlaintextEmail">
                                            <Form.Label column sm="1">
                                                Tresc
                                            </Form.Label>
                                            <Col sm="11">
                                                    <CKEditor
                                                        editor={ ClassicEditor }
                                                        data={props.post_content}
                                                        onInit={ editor => {
                                                            // You can store the "editor" and use when it is needed.
                                                            console.log(editor)
                                                            
                                                        } }
                                                        onChange={ ( e, editor ) => {
                                                            props.handleChangePostContent(e, editor)
                                                        } }
                                                    />
                                            </Col>
                                        </Form.Group>
                                    </Form>
                                </Card.Text>
                            </Card.Body> 
                        </Card>
                    </Col> 
                </Row>
            </Animated>
            </div>
        )
}

class Thread extends React.Component
{

    constructor(props) {
        super(props)

        this.state = {
            thread: {},
            author: {},
            posts: [],
            posts_loaded: false,
            categories: [],
            show_new_post_form: false,
            post_display: false,
            button_display: true,
            close_button_display: false,
            post_content: ''
        }

        this.handleClickNewPostButton = this.handleClickNewPostButton.bind(this)
        this.handleClickCloseNewPostForm = this.handleClickCloseNewPostForm.bind(this)
        this.handleChangePostContent = this.handleChangePostContent.bind(this)
    }

    componentDidMount() {
        Events.scrollEvent.register('begin', function() {
        })

        Events.scrollEvent.register('end', function () {
        })
        scroller.scrollTo('thread-content', {
          duration: 800,
          delay: 0,
          smooth: 'easeInOutQuart'
        })
        const params = this.props.match.params
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
                const posts_full = []
                posts.map((post) => {
                    post.loaded = true
                    posts_full.push(post)
                })
                this.setState({
                    posts: posts_full,
                    posts_loaded: true
                })
                console.log(posts_full)
            })
    }

    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
    }

    handleClickNewPostButton() {
            
        if (!this.state.show_new_post_form) {
            scroller.scrollTo('new-post', {
                duration: 800,
                delay: 0,
                smooth: 'easeInOutQuart'
              })
            this.setState({
                show_new_post_form: true,
                post_display: true,
                button_display: false,
                close_button_display: false
            })
            setTimeout(() => {
                this.setState( prevState => ({
                    button_display: true,
                    close_button_display: true
                }));
            }, 800)
        } else {
            this.submitPost()
        } 
    }

    handleClickCloseNewPostForm() {
        this.setState({
                show_new_post_form: false,
                button_display: false,
                close_button_display: false
            })
            setTimeout(() => {
                this.setState( prevState => ({
                    post_display: false,
                    button_display: true
                  }));
            }, 1000)
    }

    handleChangePostContent(e, editor) {
        this.setState({
            post_content: editor.getData()
        })
    }

    submitPost() {
        const access_token = localStorage.getItem('access_token')
        const payload = {
            headers: {
                Authorization: `Bearer ${access_token}`
            }
        }
        const params = this.props.match.params
        const data = {
            thread: params.threadId,
            content: this.state.post_content
        }
        api.post(`/forum/posts/`, data, payload)
            .then(response => {
                console.log(response.data)
                const posts_data = this.state.posts
                posts_data.push(response.data)
                this.handleClickCloseNewPostForm()
                this.setState({posts: posts_data})
            })
    }

    render() {
        let display_close = 'none'

        let display = 'block'

        if (!this.state.button_display) {
            display = 'none'
        }

        if (this.state.close_button_display) {
            display_close = 'block'
        }

        const { thread, author, posts } = this.state

        let thread_content = String(thread.content)
        return (
            <div id="thread-content">

                
                <Row>
                    <Col md={{span: 8, offset: 2}}>
                        <h2>{thread.title}</h2>
                        <Card key={thread.id} className="bonus-card">
                            <Card.Body className="bonus-card-bg">
                                <Card.Title>{author.username}</Card.Title>
                                <Card.Text>
                                    {Parser(thread_content)}
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
                            <Animated 
                                animationIn="fadeIn" 
                                isVisible={post.loaded} 
                            >
                                <Card key={post.id} className="bonus-card">
                                    <Card.Body className="bonus-card-bg">
                                        <Card.Title>{post.author.username}</Card.Title>
                                        <Card.Text>
                                            {Parser(post.content)}
                                        </Card.Text>
                                    </Card.Body> 
                                </Card>
                            </Animated>
                        </Col> 
                    )}
                </Row>
                <NewPostForm 
                    show_new_post_form={this.state.show_new_post_form}
                    post_display={this.state.post_display}
                    post_content={this.state.post_content}
                    handleChangePostContent={this.handleChangePostContent}
                />  
                <Row>
                    <Col md={{span: 3, offset: 7}}> 
                            <Animated 
                                animationIn="fadeIn"
                                animationOut="fadeOut" 
                                isVisible={this.state.button_display}
                                animateOnMount={false}
                            > 
                                    <Button 
                                        variant="secondary" 
                                        block
                                        onClick={this.handleClickNewPostButton}
                                        style={{display: display, marginBottom: '5px'}}
                                    >
                                        Dodaj odpowiedź
                                    </Button>
                            </Animated>
                    </Col>
                </Row>
                <Row>
                    <Col md={{span: 3, offset: 7}}>
                        <Animated 
                                animationIn="fadeIn"
                                animationOut="fadeOut" 
                                isVisible={this.state.close_button_display}
                                animateOnMount={false}
                            > 
                                    <Button 
                                        variant="secondary" 
                                        block
                                        onClick={this.handleClickCloseNewPostForm}
                                        style={{display: display_close}}
                                    >   
                                        Zamknij
                                    </Button>
                            </Animated>
                    </Col>
                </Row>
            </div>
        )
    }
}

export default withRouter(Thread)