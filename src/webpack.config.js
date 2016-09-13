var path = require('path');
var BundleTracker = require('/usr/lib/node_modules/webpack-bundle-tracker')

module.exports = {
  entry: './bundle-in.js',
  output: {
      path: path.resolve('../assets/bundles/'),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  resolve: {
    fallback: '/usr/lib/node_modules',
    root: path.resolve(__dirname),
    alias: {
      app: 'shared_goals/jsx/app',
      homepage: 'shared_goals/jsx/homepage',
      goalpage: 'shared_goals/jsx/goalpage',
      suggestionpage: 'shared_goals/jsx/suggestionpage',
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
