'use strict'

import HomePage from 'homepage'
import GoalPage from 'goalpage'
import React from 'react'
import ReactDOM from 'react-dom'
import { Router, Route, browserHistory } from 'react-router'

ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="/" component={HomePage.Page} />
    <Route path="/to/:goal_slug/" component={GoalPage.Page} />
  </Router>
), document.getElementById('root'));
