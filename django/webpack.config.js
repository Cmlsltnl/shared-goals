var path = require('path');
var webpack = require('/usr/lib/node_modules/webpack');
var BundleTracker = require('/usr/lib/node_modules/webpack-bundle-tracker')

module.exports = {
  entry: './bundle-in.js',
  output: {
      path: path.resolve('../assets/bundles/'),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'})
  ],

  resolve: {
    fallback: '/usr/lib/node_modules',
    root: [
      path.resolve(__dirname),
      path.resolve('shared_goals/jsx'),
    ],
    alias: {
    },
    extensions: ['', '.js', '.jsx']
  },

  resolveLoader: {
      fallback: '/usr/lib/node_modules'
  },

  module: {
    loaders: [
      {
        test: /.jsx?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['/usr/lib/node_modules/babel-preset-es2015', '/usr/lib/node_modules/babel-preset-react']
        }
      },
      {
        test: /\.json$/,
        loader: 'json'
      }
    ]
  },
};
