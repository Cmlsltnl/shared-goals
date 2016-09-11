var path = require('path');

module.exports = {
  entry: './bundle-in.js',
  output: { path: __dirname, filename: '../res/js/bundle.js' },

  resolve: {
    fallback: '/usr/lib/node_modules',
    root: path.resolve(__dirname),
    alias: {
      app: 'shared_goals/jsx/app',
      home: 'shared_goals/jsx/home',
      goal: 'goal/jsx/goal',
      suggestion: 'suggestion/jsx/suggestion',
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
      }
    ]
  },
};
