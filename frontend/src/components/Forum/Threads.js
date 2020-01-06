import React from 'react';
import { 
    Row, 
    Col, 
    Badge,
    Card
} from 'react-bootstrap';
import api from '../../api';

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

export default Threads