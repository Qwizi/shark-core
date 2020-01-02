import React from 'react';
import Nav from 'react-bootstrap/Nav';

class Categories extends React.Component
{
    render() {
        const { categories } = this.props
        return (
            categories.map((category) =>
                <Nav.Item key={category.pk}>
                    <Nav.Link eventKey={category.name}>
                        {category.name}
                    </Nav.Link>
                </Nav.Item>
            )
        );
    }
}

export default Categories