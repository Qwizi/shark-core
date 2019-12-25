import React from 'react';
import { Card, Row, Col, Button, Badge } from 'react-bootstrap';

class BonusCard extends React.Component
{
    render() {
        return (
            <Card className="h-100">
                <Card.Header className="sign-in-card">
                    {this.props.bonus.name}
                </Card.Header>
                <Card.Body className="bonus-card">
                    <Card.Text>
                        {this.props.bonus.description}
                    </Card.Text>
                </Card.Body>
                <Card.Footer className="bonus-card">
                    <Row>
                        <Col md={6} lg={8}>
                            <h1>
                                <Badge variant="secondary">
                                    {this.props.bonus.price}zł
                                </Badge>
                            </h1>
                        </Col>
                        <Col md={6} lg={4}>
                            <Button 
                                variant="success" size="lg" 
                                block
                                onClick={(e) => this.props.handleBonus(this.props.bonus)}
                            >
                                Wybieram
                            </Button>
                        </Col>
                    </Row>
                </Card.Footer>
            </Card>
        )
    }
}

export default BonusCard