var path = require('path');

module.exports = {
  entry: './main.js',
  output: { path: __dirname, filename: 'foobundle.js' },

  resolve: {
    fallback: '/usr/lib/node_modules'
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
      }
    ]
  },
};
