import React from "react";
import ThreadItem from "./threadItem";
import Spinner from "./spinner";


export default class Threads extends React.Component {
    render() {
        const {data} = this.props;

        if (!data || !data.results) return <Spinner/>;
        if (!data.results.length) return <ThreadItem title={'Pusto'} content={'Brak tematow'}/>;

        return (
            <>
                {data.results.map((thread) =>
                    <ThreadItem title={thread.title} content={thread.content}/>
                )}
            </>
        )
    }
}