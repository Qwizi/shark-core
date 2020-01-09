import React from 'react';
import { Col, Card } from 'react-bootstrap';
import api from '../../api';

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
            })
    }

    render() {
        const { pinned_threads } = this.state
        return (
            pinned_threads.map((thread) =>
                <Col key={thread.id} md={{span: 6}}>
                    <Card className="bonus-card-pinned">
                        <Card.Header className="bonus-card-bg">
                            {thread.title}
                        </Card.Header>
                    </Card>
                </Col> 
            )
        )
    }
}

export default PinnedThreads