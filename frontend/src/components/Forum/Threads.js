import React from 'react';
import {
    Row,
    Col,
    Badge,
    Card
} from 'react-bootstrap';
import api from '../../api';
import {Link, withRouter} from 'react-router-dom';
import querystring from "query-string";
import {CONFIG} from "../../config";

const FORUM_CATEGORIES_ENDPOINT = CONFIG.API.ENDPOINTS.FORUM.CATEGORIES;

class Threads extends React.Component {

    componentDidMount() {
        this.props.setPageName('Forum');
        const params = querystring.parse(this.props.location.search);

        if (params['category']) {
            api.get(FORUM_CATEGORIES_ENDPOINT + params['category'])
                .then(response => {
                    const name = response.data.name;
                    this.props.setPageAdditionalName(name)
                })
        }

    }

    render() {
        const {threads} = this.props;
        return (
            threads.map((thread) =>
                <Row key={thread.id}>
                    <Col md={{span: 11, offset: 1}}>
                        <Card className="bonus-card">
                            <Card.Body className="bonus-card-bg">
                                <Card.Title><Link
                                    to={`${this.props.match.url}thread/${thread.id}`}>{thread.title}</Link></Card.Title>
                                <Card.Text>
                                    {thread.content}
                                </Card.Text>
                            </Card.Body>
                            <Card.Footer className="bonus-card-footer">
                                <Row>
                                    <Col md={1}>{thread.author.username}</Col>
                                    <Col md={8}><p className="text-muted">{thread.created}</p></Col>
                                    <Col md={2}>
                                        <Badge variant="secondary">{thread.category.name}</Badge>
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

export default withRouter(Threads)