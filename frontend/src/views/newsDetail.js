import React from "react";
import PropTypes from 'prop-types';
import {Animated} from "react-animated-css";
import {Link} from "react-router-dom";


export default class NewsDetail extends React.Component {
    constructor(props) {
        super(props);

        this.data = [
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
                title: 'Test2',
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
        ];
    }

    render() {
        const newsId = this.props.match.params.id;
        const article = this.data.find(item => item.id === Number(newsId));

        return (
            <>
                <div className="row">
                    <div className="col">
                        <Animated animationIn="fadeIn" animationOut="fadeOut" isVisible={true}>
                            <div className="jumbotron jumbotron-fluid jumbotron-bg" >
                                <div className="container-fluid">
                                    <h1 className="display-6">
                                        {article.title}
                                    </h1>
                                    <p className="lead">
                                        {article.content}
                                    </p>
                                </div>
                            </div>
                        </Animated>
                    </div>
                </div>
            </>
        )
    }
}