import React from "react";
import CKEditor from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import {Animated} from "react-animated-css";

import api from "../api";
import {CONFIG} from "../config";

const initialData = {
    editorData: ''
};

export default class NewPost extends React.Component {

    constructor(props) {
        super(props);

        this.state = initialData;

        this.onClickAddNewPostButton = this.onClickAddNewPostButton.bind(this);

    }

    addPost(data) {
        return api.post(CONFIG.API.ENDPOINTS.FORUM.POSTS, data);
    }

    onClickAddNewPostButton() {
        const {threadId, authorId} = this.props;

        if (!threadId || !authorId) return;

        const dataToSend = {
            thread: threadId,
            author: authorId,
            content: this.state.editorData
        };

        this.addPost(dataToSend)
            .then((response) => {
                if (response.status === 201) {
                    console.log(response.data);
                    this.props.updatePostsData(response.data);
                }
            })
    }

    render() {
        return (
            <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={true}>
                <div className="row" style={{minHeight: '50vh'}}>
                    <div className="col-md-10 offset-md-1">
                        <div className="card card-bg">
                            <div className="card-body">
                                <div className="row">
                                    <div className="col">
                                        <CKEditor
                                            editor={ClassicEditor}
                                            data={this.state.editorData}
                                            onInit={editor => {
                                                // You can store the "editor" and use when it is needed.
                                                console.log('Editor is ready to use!', editor);
                                            }}
                                            onChange={(event, editor) => {
                                                const data = editor.getData();
                                                this.setState({editorData: data});
                                                console.log({event, editor, data});
                                            }}
                                            onBlur={(event, editor) => {
                                                console.log('Blur.', editor);
                                            }}
                                            onFocus={(event, editor) => {
                                                console.log('Focus.', editor);
                                            }}
                                        />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col">
                                        <button
                                            className="btn btn-success float-right"
                                            style={{marginTop: '10px'}}
                                            onClick={this.onClickAddNewPostButton}
                                        >
                                            Dodaj odpowiedz
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </Animated>
        )
    }
}