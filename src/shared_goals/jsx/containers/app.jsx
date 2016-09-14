'use strict'

import 'babel-polyfill'

import React from 'react'
import ReactDOM from 'react-dom'
import { Router, Route, browserHistory } from 'react-router'
import { createStore, applyMiddleware, compose } from 'redux'
import { Provider } from 'react-redux';
import appReducer from 'reducers'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'

import HomePage from 'containers/homepage'
import GoalPage from 'containers/goalpage'
import SuggestionPage from 'containers/suggestionpage'

const loggerMiddleware = createLogger()

const Root = ({ store }) => (
  <Provider store={store}>
      <Router history={browserHistory}>
        <Route path="/" component={HomePage.Page} />
        <Route path="/to/:goal_slug/" component={GoalPage.Page} />
        <Route path="/to/:goal_slug/by/:suggestion_slug" component={SuggestionPage.Page} />
      </Router>
  </Provider>
);

let store = createStore(
    appReducer,
    compose(
        applyMiddleware(
            thunkMiddleware, // lets us dispatch() functions
            loggerMiddleware // neat middleware that logs actions
        ),
        window.devToolsExtension ? window.devToolsExtension() : DevTools.instrument()
    )
)

ReactDOM.render((
    <Root store={store} />
), document.getElementById('root'));
