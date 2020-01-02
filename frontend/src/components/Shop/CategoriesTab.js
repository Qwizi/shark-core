import React from 'react'
import Tab from 'react-bootstrap/Tab'
import Row from 'react-bootstrap/Row'
import BonusCategoriesTab from './BonusCategoriesTab';

class CategoriesTab extends React.Component
{
    render() {

        const { 
            categories, 
            handleEnterTab, 
            handleBonus,
            bonuses
        } = this.props

        return (
            categories.map((category) =>
                <Tab.Pane
                    key={category.pk} 
                    eventKey={category.name}
                    onEnter={(e) => handleEnterTab(category.pk)}
                >
                    <Row>
                        <BonusCategoriesTab bonuses={bonuses} handleBonus={handleBonus}/>
                    </Row>
                </Tab.Pane>
            )
        )
    }
}

export default CategoriesTab