var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
var ExtractTextPlugin = require('extract-text-webpack-plugin');

function isDevelopmentEnvironment(){
  return process.env.NODE_ENV === 'development'
}

function buildEntry(){
  entry = {
    app: [ './javascript/src/index.js']
  }

  if (isDevelopmentEnvironment()) {
    Object.keys(entry).forEach(function (key) {
      entry[key].unshift('webpack/hot/only-dev-server');
      entry[key].unshift('webpack-dev-server/client?http://localhost:3000');
    });
  }

  return entry;
}

function buildOutput(){
  return {
    path: path.resolve(__dirname, 'public/bundles'),
    filename: "[name]-[hash].js",
    publicPath: isDevelopmentEnvironment() ?
      'http://localhost:3000/assets/bundles/' : '/static/bundles/',
  };
}

module.exports = {
    context: path.resolve(__dirname, 'app/assets/'),

    entry: buildEntry(),

    output: buildOutput(),

    plugins: [
      new webpack.HotModuleReplacementPlugin(),
      new webpack.NoErrorsPlugin(),
      new BundleTracker({filename: './webpack-stats.json'}),
      new ExtractTextPlugin('[name]-[hash].css'),
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
      }),
    ],

    module: {
      loaders: [
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          loader: 'babel',
          query: {
             presets: ['es2015', 'react']
          }
        },
        {
          test: /\.scss$/,
          loaders: ["style", "css", "sass"]
        }
      ],
    },

    resolve: {
      modulesDirectories: ['node_modules'],
      extensions: ['', '.js', '.jsx']
    }
};
