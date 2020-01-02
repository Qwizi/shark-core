import React from 'react';
import { Row, Col, Tab, Nav } from 'react-bootstrap';
import { CategoriesTab, Categories } from '../components/Shop/'
import api from '../api';

const API_URLS = {
    CATEGORIES: '/store/categories/',
    BONUSES: '/store/bonuses/'
}

export default class Shop extends React.Component
{
    constructor(props) {
        super(props);
        this.state = {
            categories: [],
            bonuses: [],
        }
        this.handleOnCategoryEnterTab = this.handleOnCategoryEnterTab.bind(this)
    }

    async getCategories() {
        const response = await api.get(API_URLS.CATEGORIES)
        const categories = response.data.results

        return Promise.resolve(categories)
    }

    async getBonuses(category_pk) {
        const response = await api.get(API_URLS.BONUSES+`?category=${category_pk}`)
        const bonuses = response.data.results

        return Promise.resolve(bonuses)
    } 

    async componentDidMount() {
        const categories = await this.getCategories()
        this.setState({categories: categories})
    }

    async handleOnCategoryEnterTab(category_pk) {
        category_pk = Number(category_pk)
        const bonuses = await this.getBonuses(category_pk)
        this.setState({bonuses: bonuses})
    }

    render() {

        return (
            <div>
            <Row>
                <Col><h2>Kategorie: </h2></Col>
            </Row>
            <Row>
                <Tab.Container>
                        <Col md={2}>
                            <Nav variant="pills" className="flex-column">
                                <Categories 
                                    categories={this.state.categories}
                                />
                            </Nav>
                        </Col>
                        <Col md={10}>
                            <Tab.Content>
                                <CategoriesTab 
                                    categories={this.state.categories}
                                    handleEnterTab={this.handleOnCategoryEnterTab}
                                    bonuses={this.state.bonuses}
                                />
                            </Tab.Content>
                        </Col>
                </Tab.Container>
            </Row>
            </div>
        );
    }
}