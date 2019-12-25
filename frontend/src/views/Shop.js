import React from 'react';
import axios from 'axios';
import { Row, Col, Tab, Nav } from 'react-bootstrap';
import { CategoriesTab, Categories } from '../components/Shop/'

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

    componentDidMount() {
        axios.get(`http://localhost:8000/api/store/categories/`)
        .then(res => {
            const categories = res.data;
            this.setState({categories: categories.results})
        })
    }

    handleOnCategoryEnterTab(category_pk) {
        category_pk = Number(category_pk)
        axios.get(`http://localhost:8000/api/store/bonuses/?category=${category_pk}`)
        .then(res => {
            const bonuses = res.data;
            this.setState({bonuses: bonuses.results})
        })
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