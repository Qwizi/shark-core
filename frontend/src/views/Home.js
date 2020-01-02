import React from 'react'
import { Row, Col, Table } from 'react-bootstrap';
import api from '../api'


class ServersRow extends React.Component
{

    componentDidMount() {
        console.log(this.props.servers)
    }

    render() {

        const { servers } = this.props

        return (
            servers.map((server, index) =>
                <tr>
                    <td>{server.name}</td>
                </tr>
            )
        )
    }
}

class ServersTable extends React.Component
{

    constructor(props) {
        super(props)
        this.state = {
            servers: []
        }
    }

    async getServers() {
        const response = await api.get('/servers/')
        const servers = response.data.results
        return Promise.resolve(servers)
    }

    async getServerStatus(server_id) {
        const response = await api.get(`/servers/${server_id}/status/`)
        const status = response.data
        return Promise.resolve(status)
    }

    async componentDidMount() { 
        this.getServers().then(servers => {
            const servers_full = []
            servers.map((server) => {
                this.getServerStatus(server.id)
                    .then(status => {
                        const server_new = status
                        servers_full.push(server_new)
                    })
            })
            this.setState({servers: servers_full})
            console.log(this.state.servers)
        })
    }

    render() {
        return (
            <Table responsive striped bordered hover variant="dark">
                <thead>
                    <tr>
                        <th>game</th>
                        <th>name</th>
                        <th>ip</th>
                        <th>players</th>
                        <th>map</th>
                    </tr>
                </thead>
                <tbody>
                    <ServersRow servers={this.state.servers}/>
                </tbody>
            </Table>
        )
    }
}

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
    render() {
        const { username, logged } = this.props.user
        return (
            <div>
                <Row className="justify-content-center">
                    <Col md="auto">
                        <ServersTable />
                        <HelloMsg logged={logged} username={username} />
                    </Col>
                </Row>
            </div>
        )
    }
}

export default Home