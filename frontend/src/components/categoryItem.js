import React from "react";
import PropTypes from 'prop-types';
import {Link} from "react-router-dom";

export default class CategoryItem extends React.Component
{
    render() {
        const {id, name, subcategories} = this.props;
        return (
            <li className="nav-item">
                <div className="btn-group btn-group-sm" style={{marginBottom: '10px', marginRight: '10px'}}>
                    <Link
                        to={`/forum/category/${id}/`}
                        className="btn btn-primary btn-sm"
                    >
                        {name}
                    </Link>
                    {subcategories && subcategories.length > 0 && (
                        <>
                            <button className="btn btn-sm btn-primary dropdown-toggle dropdown-toggle-split"
                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <span className="sr-only">Toggle Dropdown</span>
                            </button>
                            <div className="dropdown-menu">
                                {subcategories.map((subcategory) =>
                                    <Link
                                        to={`/forum/category/${id}-${subcategory.id}/`}
                                        className="dropdown-item"
                                    >
                                        {subcategory.name}
                                    </Link>
                                    )
                                }
                            </div>
                        </>
                    )}
                </div>
            </li>
        )
    }
}

CategoryItem.defaultProps = {
    id: 1,
    name: 'Default category'
};

CategoryItem.propTypes = {
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired
};