import React from "react";
import CategoryItem from "./categoryItem";
import Spinner from "./spinner";

export default class Categories extends React.Component {
    render() {
        const {data} = this.props;

        if (!data || !data.results) return <Spinner center={false}/>;
        if (!data.results.length) return <span>Brak kategorii</span>;


        return (
            <>
                {data.results.map((category) =>
                    <CategoryItem id={category.id} name={category.name}/>
                )}
            </>
        )
    }
}

Categories.defaultProps = {
    data: {}
};