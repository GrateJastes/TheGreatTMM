import React from 'react';
import * as ReactDOM from 'react-dom';
import './style/base.scss';
import { App } from './components/app/App.jsx';

function main() {
  ReactDOM.render(
    <App/>,
    document.getElementById('app'),
  );
}

main();
