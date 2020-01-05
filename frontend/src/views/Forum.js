import React from 'react';
import { 
    Row, 
    Col, 
    Badge, 
    Tab, 
    Nav,
    Button,
    Card
} from 'react-bootstrap';
import api from '../api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';

class PinnedThreads extends React.Component
{
    constructor(props) {
        super(props)

        this.state = {
            pinned_threads: []
        }
    }

    componentDidMount() {
        api.get('/forum/threads/?pinned')
            .then(response => {
                const threads = response.data.results
                this.setState({
                    pinned_threads: threads
                })
                console.log(threads)
            })
    }

    render() {
        const { pinned_threads } = this.state
        return (
            pinned_threads.map((thread) =>
                <Col md={{span: 6}}>
                    <Card key={thread.id} className="bonus-card-pinned">
                        <Card.Header className="bonus-card-bg">
                            {thread.title}
                        </Card.Header>
                    </Card>
                </Col> 
            )
        )
    }
}

class Threads extends React.Component
{
    constructor(props) {
        super(props)

        this.state = {
            threads: []
        }
    }

    componentDidMount() {
        api.get('/forum/threads/')
            .then(response => {
                const threads = response.data.results
                this.setState({
                    threads: threads
                })
                console.log(threads)
            })
    }

    render() {
        const { threads } = this.state
        return (
            threads.map((thread) =>
            <Row>
                <Col md={{span: 11, offset: 1}}>
                    <Card key={thread.id} className="bonus-card">
                        <Card.Body className="bonus-card-bg">
                            <Card.Title>{thread.title}</Card.Title>
                            <Card.Text>
                                {thread.content}
                            </Card.Text>
                        </Card.Body>
                        <Card.Footer className="bonus-card-footer">
                            <Row>
                                <Col md={1}>{thread.author.username}</Col>
                                <Col md={8}><p className="text-muted">{thread.created}</p></Col>
                                <Col md={2}>
                                {thread.categories.map((category) =>
                                    <Badge variant="secondary">{category.name}</Badge>
                                )}
                                </Col>
                            </Row>
                        </Card.Footer>
                    </Card>
                </Col> 
            </Row>
            )
        )
    }
}


class Categories extends React.Component
{
    constructor(props) {
        super(props)

        this.state = {
            categories: []
        }
    }

    componentDidMount() {
        api.get('/forum/categories/')
            .then(response => {
                const categories = response.data.results
                this.setState({categories: categories})
                console.log(categories)
            })
    }

    render() {
        const { categories } = this.state
        return (
            categories.map((category) =>
                <Nav.Item key={category.id}>
                    <Nav.Link eventKey={category.name}>
                        {category.name}
                    </Nav.Link>
                </Nav.Item>
            )
        )
    }
}

class Forum extends React.Component
{
    componentDidMount() {
        this.props.setPageName('Forum')
    }

    render() {
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
                    </Col>
                </Row>
            </div>
        )
    }
}

export default Forum