import React from 'react'
import { Nav } from 'react-bootstrap';
import api from '../../api';
import { NavLink, withRouter } from 'react-router-dom';

class Categories extends React.Component
{
    constructor(props) {
        super(props)

        this.state = {
            categories: []
        }

        this.onClickNav = this.onClickNav.bind(this)
    }

    componentDidMount() {
        api.get('/forum/categories/')
            .then(response => {
                const categories = response.data.results
                this.setState({categories: categories})
            })
        console.log(this.props.match.path)
    }

    componentWillUnmount() {
        this.props.setPageAdditionalName(null)
    }

    onClickNav(category_id, category_name) {
        this.props.getThreads(category_id)
        this.props.setCategoryName(category_name)
        this.props.setPageAdditionalName(category_name)
        this.props.setThreadIsLoadedFalse()
        console.log(category_name)
    }

    render() {

        const { path } = this.props.match
        const { categories } = this.state
        return (
            categories.map((category) =>
                <Nav.Item key={category.id}>
                    <NavLink to={`${path}threads/?category=${category.id}`} onClick={() => this.onClickNav(category.id, category.name)}>
                        {category.name}
                    </NavLink>
                </Nav.Item>
            )
        )
    }
}

export default withRouter(Categories)