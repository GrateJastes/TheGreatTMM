import React from 'react';
import { constants as consts } from '../../consts/consts.js';
import './uploadView.scss';
import uploadIcon from './upload.png';

export class UploadView extends React.Component {
  constructor(props) {
    super(props);
    this.state = { videoLoaded: false };
  }

  handleNextClick = () => {
    this.props.changeView(consts.views.uploadView);
  }

  handleBackClick = () => {
    this.props.changeView(consts.views.welcomeView);
  }

  previewVideo = (event) => {
    event.preventDefault();

    const file = document.getElementById('file-input').files;

    if (file.length > 0) {
      const fileReader = new FileReader();

      fileReader.onload = (event) => {
        document.getElementById('video-source').src = event.target.result;
        document.getElementById('preview-video').style.display = 'block';
      };

      console.log(file[0]);
      fileReader.readAsDataURL(file[0]);

      document.querySelector('.upload__preview-icon').style.display = 'none';
      document.querySelector('.upload__preview-label').style.backgroundColor = 'transparent';
    }
  }

  render() {
    const nextButtonClasses = `upload__navigation-button ${this.state.videoLoaded ? '' : 'upload__navigation-button_inactive'}`;
    return (
      <div className="upload">
        <form className="upload__form">
          <h1 className="upload__title">Загрузите видео</h1>
          <label htmlFor="file-input" className="upload__preview-label" id="preview-label">
            <div className="upload__preview-box">
              <video id="preview-video" className="upload__preview-video">
                <source id="video-source" type="video"/>
              </video>
              <img src={uploadIcon} alt="upload" className="upload__preview-icon"/>
            </div>
          </label>
          <input onChange={this.previewVideo} id="file-input" type="file" className="upload__file-input"/>
          <div className="upload__video-requirements">
            Видео должно быть 600x500 и 30fps минимум
          </div>
          <div className="upload__error-box upload__error-box_hidden">
            Видео не соответствует требованиям
          </div>
        </form>
        <div className="upload__navigation-footer">
          <button onClick={this.handleBackClick} className="upload__navigation-button">Назад</button>
          <button
            onClick={this.handleNextClick}
            className={nextButtonClasses}>
            Далее
          </button>
        </div>
      </div>
    );
  }
}
