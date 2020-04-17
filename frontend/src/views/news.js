import React from "react";
import {Switch, Route, withRouter} from 'react-router-dom';
import {ArticleCard} from "../components/acticle";
import {NewsDetail} from "./index";

const initialState = {
    data: [
        {
            id: 1,
            title: 'Test',
            content: 'Lorem Ipsum jest tekstem stosowanym jako przykładowy wypełniacz w przemyśle\n' +
                '                                    poligraficznym. Został po raz pierwszy użyty w XV w. przez nieznanego drukarza do\n' +
                '                                    wypełnienia tekstem próbnej książki. Pięć wieków później zaczął być używany\n' +
                '                                    przemyśle elektronicznym, pozostając praktycznie niezmienionym. Spopularyzował się w\n' +
                '                                    latach 60. XX w. wraz z publikacją arkuszy Letrasetu, zawierających fragmenty Lorem\n' +
                '                                    Ipsum, a ostatnio z zawierającym różne wersje Lorem Ipsum oprogramowaniem\n' +
                '                                    przeznaczonym do realizacji druków na komputerach osobistych, jak Aldus PageMaker'
        },
        {
            id: 2,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem, czyli ponad 2000 lat temu! Richard McClintock, wykładowca łaciny na uniwersytecie Hampden-Sydney w Virginii, przyjrzał się uważniej jednemu z najbardziej niejasnych słów w Lorem Ipsum – consectetur – i po wielu poszukiwaniach odnalazł niezaprzeczalne źródło: Lorem Ipsum pochodzi z fragmentów (1.10.32 i 1.10.33) „de Finibus Bonorum et Malorum”, czyli „O granicy dobra i zła”, napisanej właśnie w 45 p.n.e. przez Cycerona. Jest to bardzo popularna w czasach renesansu rozprawa na temat etyki. Pierwszy wiersz Lorem Ipsum, „Lorem ipsum dolor sit amet...” pochodzi właśnie z sekcji 1.10.32.\n' +
                '\n' +
                'Standardowy blok Lorem Ipsum, używany od XV wieku, jest odtworzony niżej dla zainteresowanych. Fragmenty 1.10.32 i 1.10.33 z „de Finibus Bonorum et Malorum” Cycerona, są odtworzone w dokładnej, oryginalnej formie, wraz z angielskimi tłumaczeniami H. Rackhama z 1914 roku.' +
                'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem, czyli ponad 2000 lat temu! Richard McClintock, wykładowca łaciny na uniwersytecie Hampden-Sydney w Virginii, przyjrzał się uważniej jednemu z najbardziej niejasnych słów w Lorem Ipsum – consectetur – i po wielu poszukiwaniach odnalazł niezaprzeczalne źródło: Lorem Ipsum pochodzi z fragmentów (1.10.32 i 1.10.33) „de Finibus Bonorum et Malorum”, czyli „O granicy dobra i zła”, napisanej właśnie w 45 p.n.e. przez Cycerona. Jest to bardzo popularna w czasach renesansu rozprawa na temat etyki. Pierwszy wiersz Lorem Ipsum, „Lorem ipsum dolor sit amet...” pochodzi właśnie z sekcji 1.10.32.\n' +
                '\n' +
                'Standardowy blok Lorem Ipsum, używany od XV wieku, jest odtworzony niżej dla zainteresowanych. Fragmenty 1.10.32 i 1.10.33 z „de Finibus Bonorum et Malorum” Cycerona, są odtworzone w dokładnej, oryginalnej formie, wraz z angielskimi tłumaczeniami H. Rackhama z 1914 roku.' +
                'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem, czyli ponad 2000 lat temu! Richard McClintock, wykładowca łaciny na uniwersytecie Hampden-Sydney w Virginii, przyjrzał się uważniej jednemu z najbardziej niejasnych słów w Lorem Ipsum – consectetur – i po wielu poszukiwaniach odnalazł niezaprzeczalne źródło: Lorem Ipsum pochodzi z fragmentów (1.10.32 i 1.10.33) „de Finibus Bonorum et Malorum”, czyli „O granicy dobra i zła”, napisanej właśnie w 45 p.n.e. przez Cycerona. Jest to bardzo popularna w czasach renesansu rozprawa na temat etyki. Pierwszy wiersz Lorem Ipsum, „Lorem ipsum dolor sit amet...” pochodzi właśnie z sekcji 1.10.32.\n' +
                '\n' +
                'Standardowy blok Lorem Ipsum, używany od XV wieku, jest odtworzony niżej dla zainteresowanych. Fragmenty 1.10.32 i 1.10.33 z „de Finibus Bonorum et Malorum” Cycerona, są odtworzone w dokładnej, oryginalnej formie, wraz z angielskimi tłumaczeniami H. Rackhama z 1914 roku.'
        },
        {
            id: 3,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 4,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 5,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 6,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 7,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 8,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 9,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 10,
            title: 'Test sad as das as asdasd asdsadasddddd623432432',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
    ],
    data2: [
        {
            id: 11,
            title: '11',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
        {
            id: 12,
            title: '12',
            content: 'Skąd się to wzięło?\n' +
                'W przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem,'
        },
    ]
};

class News extends React.Component {
    constructor(props) {
        super(props);

        this.state = initialState;
    }

    handleClick(e) {
        const data = this.state.data;
        const data2 = this.state.data2;
        const updatedData = data.concat(data2);
        this.setState({data: updatedData});
    }

    render() {
        const {data} = this.state;
        const {match} = this.props;
        return (
            <Switch>
                <Route exact path={`${match.path}`}>
                    <ArticleCard data={data}/>
                    <div className="row">
                        <div className="col text-center">
                            <button
                                className="btn btn-success btn-lg btn-block"
                                onClick={(e) => this.handleClick(e)}
                            >
                                Show more
                            </button>
                        </div>
                    </div>
                </Route>
                <Route path={`${match.path}/:id`}>
                    <NewsDetail/>
                </Route>
            </Switch>
        )
    }
}

export default withRouter(News);
