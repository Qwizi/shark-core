import React from 'react'
import { Row, Col, Table } from 'react-bootstrap';
import api from '../api'


class HelloMsg extends React.Component
{
    render() {
        const { username, logged } = this.props
        if (logged) {
            return (
                <h1>Witaj, {username}</h1>
            )
        } else {
            return (
                <h1>Witaj na sharkCore</h1>
            )
        }
    }
}

class Home extends React.Component
{

    componentDidMount() {
        this.props.setPageName('Home')
    }

    render() {
        const { username, logged } = this.props.user
        return (
            <div>
                <Row className="justify-content-center">
                    <Col md="auto">
                        <HelloMsg logged={logged} username={username} />
                    </Col>
                </Row>
            </div>
        )
    }
}

export default Home