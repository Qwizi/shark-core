import React from 'react'
import Col from 'react-bootstrap/Col'
import BonusCard from './BonusCard'
import ProgressBar from 'react-bootstrap/ProgressBar'


class BonusCategoriesTab extends React.Component
{

    constructor(props) {
        super(props)

        this.state = {
            percent: 0,
            show_msg: false
        }

        this.increse = this.increse.bind(this)
    }

    increse() {
        const { percent } = this.state
        const newPercent = percent + 1
        if (newPercent >= 100) {
            clearTimeout(this.tm)
            this.setState({show_msg: true})
            return;
        }
        this.setState((state) => ({
            percent: state.percent + 1
        }))
        this.tm = setTimeout(this.increse, 20);
    }

    componentDidMount() {
        this.increse()
    }

    render() {
        const { bonuses, handleBonus } = this.props
        
        if (bonuses.length <= 0) {
            const { percent, show_msg } = this.state
            if (show_msg) {
                return (
                    <Col><h1>Brak</h1></Col>
                )
            }

            return (
                <Col>
                    <br/><ProgressBar animated={true} now={percent} label={`${percent}%`}/>
                </Col>
            )
            
        } else {
            return (
                bonuses.map((bonus) => 
                    <Col key={bonus.id}>
                        <BonusCard bonus={bonus} handleBonus={handleBonus}/>
                    </Col>
                )
            )
        }
    }
}

export default BonusCategoriesTab