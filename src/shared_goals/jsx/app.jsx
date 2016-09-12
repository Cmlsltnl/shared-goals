'use strict'

import Goal from 'goal'
import Site from 'site'
import React from 'react'
import ReactDOM from 'react-dom'
import { Router, Route, browserHistory } from 'react-router'


const Container = (props) => <div><h1>hello</h1><Goal.Homer2 /></div>

ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="/" component={Site.Home} />
    <Route path="/by/:goal_slug/" component={Site.Goal} />
  </Router>
), document.getElementById('root'));
