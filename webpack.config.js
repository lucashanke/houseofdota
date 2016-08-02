var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: {
    app: [
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      './app/assets/javascript/src/index.js'
    ]
  },

  output: {
      path: path.resolve('./app/assets/bundles/'),
      filename: "[name]-[hash].js",
      publicPath: 'http://localhost:3000/assets/bundles/',
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),
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
      }
    ],
  },

  resolve: {
    modulesDirectories: ['node_modules'],
    extensions: ['', '.js', '.jsx']
  },
}
