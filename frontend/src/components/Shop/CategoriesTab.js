import React from 'react'
import Tab from 'react-bootstrap/Tab'
import Row from 'react-bootstrap/Row'
import BonusCategoriesTab from './BonusCategoriesTab';

class CategoriesTab extends React.Component
{
    render() {
        return (
            this.props.categories.map((category) =>
                <Tab.Pane
                    key={category.pk} 
                    eventKey={category.name}
                    onEnter={(e) => this.props.handleEnterTab(category.pk)}
                >
                    <Row>
                        <BonusCategoriesTab bonuses={this.props.bonuses} handleBonus={this.props.handleBonus}/>
                    </Row>
                </Tab.Pane>
            )
        )
    }
}

export default CategoriesTab