import React from 'react';
import { constants as consts } from 'consts/consts.js';
import { WelcomeView } from '../../views/welcomeView/WelcomeView.jsx';
import { UploadForm } from '../uploadForm/UploadForm.jsx';
import { UploadView } from '../../views/uploadView/UploadView.jsx';

export class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentView: consts.views.welcomeView,
    };
  }

  changeView = (viewName) => {
    this.setState({ currentView: viewName });
  }

  render() {
    return (
      <div className="page">
        {
          {
            'welcome-view': <WelcomeView changeView={this.changeView}/>,
            'upload-view': <UploadView changeView={this.changeView}/>,
          }[this.state.currentView]
        }
      </div>
    );
  }
}
