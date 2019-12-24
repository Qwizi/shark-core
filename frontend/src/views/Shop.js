import React from 'react';
import axios from 'axios';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Tab from 'react-bootstrap/Tab';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import Badge from 'react-bootstrap/Badge';
import Button from 'react-bootstrap/Button';
import StoreModal from './Modal';

export default class Shop extends React.Component
{
    constructor(props) {
        super(props);
        this.state = {
            categories: [],
            bonuses: [],
            show_modal: false,
            bonus: []
        }
        // this.closeModal = this.closeModal.bind(this)
    }

    setCategories() {
        axios.get(`http://localhost:8000/api/store/categories/`)
        .then(res => {
            const categories = res.data;
            this.setState({categories: categories.results})
            console.log(this.state.categories)
        })
    }

    componentDidMount() {
        this.setCategories()
    }

    handleEnterTab(category_pk) {
        category_pk = Number(category_pk)
        axios.get(`http://localhost:8000/api/store/bonuses/?category=${category_pk}`)
        .then(res => {
            const bonuses = res.data;
            this.setState({bonuses: bonuses.results})
        })
    }

    showModal(value) {
        this.setState({show_modal: value})
    }

    closeModal() {
        this.showModal(false);
    }

    handleBonus(bonus) {
        this.showModal(true);
        this.setState({bonus: bonus})
        console.log(bonus)
    }

    render() {

        return (
            <div>
            <Row>
                <Col><h2>Kategorie: </h2></Col>
            </Row>
            <Row>
                <Tab.Container onSelect={this.handleSelectTab}>
                        <Col md={2}>
                            <Nav variant="pills" className="flex-column">
                                <div id="categories-nav"></div>
                                { this.state.categories.map(category => 
                                    <Nav.Item key={category.pk}>
                                        <Nav.Link eventKey={category.name}>{category.name}
                                        </Nav.Link>
                                    </Nav.Item>
                                )}
                            </Nav>
                        </Col>
                        <Col md={10}>
                            <Tab.Content>
                                { this.state.categories.map(category => 
                                    <Tab.Pane
                                        id="1"
                                        key={category.pk} 
                                        eventKey={category.name}
                                        onEnter={(e) => this.handleEnterTab(category.pk)}
                                    >
                                    <Row>
                                    { this.state.bonuses.map(bonus =>
                                        <Col key={bonus.id}>
                                        
                                            <Card className="h-100">
                                                <Card.Header className="sign-in-card">{bonus.name}</Card.Header>
                                                <Card.Body className="bonus-card">
                                                    <Card.Text>
                                                        {bonus.description}
                                                    </Card.Text>
                                                </Card.Body>
                                                <Card.Footer className="bonus-card">
                                                    <Row>
                                                        <Col md={6} lg={8}>
                                                            <h1>
                                                                <Badge variant="secondary">
                                                                    {bonus.price}zł
                                                                </Badge>
                                                            </h1>
                                                        </Col>
                                                        <Col md={6} lg={4}>
                                                            <Button 
                                                                variant="success" size="lg" 
                                                                block
                                                                onClick={this.handleBonus.bind(this, bonus)}
                                                            >
                                                                Wybieram
                                                            </Button>
                                                        </Col>
                                                    </Row>
                                                </Card.Footer>
                                            </Card>
                                        </Col>
                                    )}
                                    </Row>
                                    </Tab.Pane>  
                                )}
                            </Tab.Content>
                        </Col>
                </Tab.Container>
            </Row>
            <StoreModal 
                show_modal={this.state.show_modal}
                bonus={this.state.bonus}
                closeModal={this.closeModal.bind(this)}
            /> 
            </div>
        );
    }
}