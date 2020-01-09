import React from 'react';
import { Row, Col, Card, Form, Button } from 'react-bootstrap';
import { Animated } from "react-animated-css";
import { Events, scroller } from 'react-scroll'
import CKEditor from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import api from '../api'

const editor_config = {
    placeholder: 'Treść'
}

class NewThread extends React.Component
{

    constructor(props) {
        super(props)

        this.state = {
            title: '',
            content: '',
            categories: []
        }

        this.handleChangeTitle = this.handleChangeTitle.bind(this)
        this.handleChangeContent = this.handleChangeContent.bind(this)
    }

    componentDidMount() {
        scroller.scrollTo('thread-content', {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuart'
          })
        api.get('/forum/categories/')
          .then(response => {
              const categories = response.data.results
              this.setState({categories: categories})
          })
        this.props.setNewThreadRedirectFalse()
    }

    handleChangeTitle(e) {
        this.setState({title: e.target.value})
    }

    handleChangeContent(e, editor) {
        console.log(editor)
        const data = editor.getData();
        this.setState({content: data})
    }

    render() {
            return (
                <div id="thread-content">

                    <Animated 
                        animationIn="fadeIn" 
                        isVisible={true}
                    >
                    <Row>
                        <Col md={{span: 8, offset: 2}}>
                            <Card className="bonus-card">
                                <Card.Body className="bonus-card-bg">
                                    <Card.Title>Nowy wątek</Card.Title>
                                    <Card.Text>
                                        <Form>
                                            <Form.Group as={Row} controlId="formPlaintextEmail">
                                                <Form.Label column sm="1">
                                                    Tytuł
                                                </Form.Label>
                                                <Col sm="4">
                                                    <Form.Control 
                                                            type="text" 
                                                            placeholder="Tytuł..."
                                                            onChange={this.handleChangeTitle}
                                                            value={this.state.title}
                                                            autoFocus={true}
                                                        />
                                                </Col>
                                                <Col sm="8"></Col>
                                            </Form.Group>
                                            <Form.Group as={Row} controlId="formPlaintextEmail">
                                                <Form.Label column sm="1">
                                                    Kategoria
                                                </Form.Label>
                                                <Col sm="4">
                                                    <Form.Control as="select">
                                                        {this.state.categories.map((category) =>
                                                        <option value={category.id}>{category.name}</option>
                                                        )}
                                                    </Form.Control>
                                                </Col>
                                                <Col sm="6"></Col>
                                            </Form.Group>
                                            <Form.Group as={Row} controlId="formPlaintextEmail">
                                                <Form.Label column sm="1">
                                                    Tresc
                                                </Form.Label>
                                                <Col sm="11">
                                                        <CKEditor
                                                            editor={ ClassicEditor }
                                                            data={this.state.content}
                                                            onInit={ editor => {
                                                                // You can store the "editor" and use when it is needed.
                                                                console.log(editor)
                                                            } }
                                                            onChange={this.handleChangeContent}
                                                            config={editor_config}
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
}

export default NewThread