import React from 'react'
import Col from 'react-bootstrap/Col'
import BonusCard from './BonusCard'

class BonusCategoriesTab extends React.Component
{
    render() {
        return (
            this.props.bonuses.map((bonus) => 
                <Col key={bonus.id}>
                    <BonusCard bonus={bonus} handleBonus={this.props.handleBonus}/>
                </Col>
            )
        )
    }
}

export default BonusCategoriesTab