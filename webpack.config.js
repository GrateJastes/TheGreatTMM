const path = require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const debug = process.env.DEBUG === 'true';
const port = process.env.PORT || 3000;
const babelOptions = JSON.parse(fs.readFileSync(path.resolve('./.babelrc.json')).toString());

module.exports = {
  mode: debug ? 'development' : 'production',
  entry: path.resolve('public/index.jsx'),
  output: {
    path: path.resolve(__dirname, 'dist'),
    // publicPath: '/',
    filename: 'index_bundle.js',
  },
  resolve: {
    alias: {
      consts: path.resolve('public/consts'),
      views: path.resolve('public/views'),
    },
    extensions: ['.jsx', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(jpg|jpeg|png|ico|ttf)$/,
        loader: 'file-loader',
      },
      {
        test: /\.(js|jsx)$/,
        exclude: /(.*node_modules)/,
        use: {
          loader: 'babel-loader',
          options: babelOptions,
        },
      },
    ],
  },
  plugins: [
    new webpack.ProgressPlugin(),
    new HtmlWebpackPlugin({
      template: path.resolve('public/index.html'),
      // favicon: path.resolve('src/assets/img/favicon.png'),
      filename: 'index.html',
    }),
    new CleanWebpackPlugin(),
    new webpack.DefinePlugin({
      DEBUG: debug,
    }),
  ],

  devServer: {
    host: '0.0.0.0',
    port,
    publicPath: '/',
    contentBase: path.resolve('public'),

    hot: debug,
    inline: debug,
    clientLogLevel: debug ? 'debug' : 'silent',
    writeToDisk: true,

    historyApiFallback: true,
    disableHostCheck: true,
  },
  devtool: 'eval-source-map',
  optimization: {
    minimize: true,
  },
};
