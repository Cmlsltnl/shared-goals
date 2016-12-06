import 'babel-polyfill'

import React from 'react'
import ReactDOM from 'react-dom'
import { IndexRoute, Router, Route, browserHistory } from 'react-router'
import { createStore, applyMiddleware, compose } from 'redux'
import { Provider } from 'react-redux';
import appReducer from 'reducers'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import Cookies from 'js-cookie'

import HomePage from 'containers/homepage'
import AppFrame from 'containers/appframe'
import GoalPage from 'containers/goalpage'
import NewGoalPage from 'containers/newgoalpage'
import SuggestionPage from 'containers/suggestionpage'
import NewSuggestionPage from 'containers/newsuggestionpage'
import EditSuggestionPage from 'containers/editsuggestionpage'

const loggerMiddleware = createLogger()

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});

const Root = ({ store }) => (
  <Provider store={store}>
      <Router history={browserHistory}>
        <Route path="/" component={AppFrame.Frame} >
            <IndexRoute component={HomePage.Page} />
            <Route path="/to/:goal_slug/" component={GoalPage.Page} />
            <Route path="/new-goal/" component={NewGoalPage.Page} />
            <Route path="/to/:goal_slug/by/:suggestion_slug/" component={SuggestionPage.Page} />
            <Route path="/to/:goal_slug/new-suggestion/" component={NewSuggestionPage.Page} />
            <Route
                path="/to/:goal_slug/by/:suggestion_slug/edit-suggestion/"
                component={EditSuggestionPage.Page}
            />
        </Route>
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
        window.devToolsExtension ? window.devToolsExtension() : f => f
    )
)

ReactDOM.render((
    <Root store={store} />
), document.getElementById('root'));
