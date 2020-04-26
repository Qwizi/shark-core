import React from "react";
import Spinner from "./spinner";
import ArticleItem from "./articleItem";


export default class Articles extends React.Component
{
    render() {
        const {data} = this.props;

        if (!data || !data.results) return <Spinner />;
        if (!data.results.length) return <ArticleItem article={{id: 0, content: 'Pusto'}}/>;

        return (
            <>
                {data.results.map((article) =>
                    <ArticleItem article={article} />
                )}
            </>
        )
    }
}