var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    context: path.resolve(__dirname, 'app/assets/'),

    entry: {
      app: [
        'webpack-dev-server/client?http://localhost:3000',
        'webpack/hot/only-dev-server',
        './javascript/src/index.js'
      ]
    },

    output: {
      path: path.resolve(__dirname, 'public/bundles'),
      filename: "[name]-[hash].js",
      publicPath: process.env.NODE_ENV === 'development' ?
        'http://localhost:3000/assets/bundles/' : '/static/',
    },

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
