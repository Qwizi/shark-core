import React from 'react'
import {Nav} from 'react-bootstrap';
import api from '../../api';
import {NavLink, withRouter} from 'react-router-dom';
import {CONFIG} from "../../config";

const FORUM_CATEGORIES_ENDPOINT = CONFIG.API.ENDPOINTS.FORUM.CATEGORIES;

class Categories extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            categories: []
        };

        this.onClickNav = this.onClickNav.bind(this)
    }

    componentDidMount() {
        api.get(FORUM_CATEGORIES_ENDPOINT)
            .then(response => {
                const categories = response.data.results;
                this.setState({categories: categories})
            })
    }

    componentWillUnmount() {
        this.props.setPageAdditionalName(null)
    }

    onClickNav(category_id, category_name) {
        this.props.getThreads(category_id);
        this.props.setCategoryName(category_name);
        this.props.setPageAdditionalName(category_name);
        this.props.setThreadIsLoadedFalse();
    }

    render() {

        const {path} = this.props.match
        const {categories} = this.state
        return (
            categories.map((category) =>
                <Nav.Item key={category.id}>
                    <NavLink to={`${path}?category=${category.id}`}
                             onClick={() => this.onClickNav(category.id, category.name)}>
                        {category.name}
                    </NavLink>
                </Nav.Item>
            )
        )
    }
}

export default withRouter(Categories)