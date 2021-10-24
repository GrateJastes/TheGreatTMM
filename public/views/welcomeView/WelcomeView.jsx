import React from 'react';
import './welcomeView.scss';
import * as ReactDOM from 'react-dom';
import { constants as consts } from 'consts/consts.js';

export class WelcomeView extends React.Component {
  handleNextClick = () => {
    this.props.changeView(consts.views.uploadView)
  }

  render() {
    return (
      <div className="title">
        <h1 className="title__header">
          Определение параметров кинематики моделей плоских рычажных механизмов
        </h1>
        <p className="title__description">
          Данная программа упростит исследование плоского рычажного механизма, упостроит траектории точек, графики функций положения, графики аналогов скоростей и ускорений и
          выведет полученные значения скоростей и ускорений точек.
          <br/>
          <br/>
          Для получения результатов кинематического анализа механизма следуйте дальнейшей инструкции.
        </p>
        <button onClick={this.handleNextClick} className="title__next-btn">Далее</button>
      </div>
    );
  }
}
