import React from 'react'
import { Nav } from 'react-bootstrap';
import api from '../../api';

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

export default Categories