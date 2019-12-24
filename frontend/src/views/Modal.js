import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

export default class StoreModal extends React.Component
{

    render() {
        return (
            <div>
            <Modal size="lg" show={this.props.show_modal} onHide={this.props.closeModal}>
                <Modal.Header closeButton className="sign-in-card">
                <Modal.Title>{this.props.bonus.name}</Modal.Title>
                </Modal.Header>
                <Modal.Body className="bonus-card">{this.props.bonus.description}</Modal.Body>
                <Modal.Footer className="bonus-card">
                <Button variant="secondary">
                    Kupuje
                </Button>
                </Modal.Footer>
            </Modal>
            </div>
        );
    }
}