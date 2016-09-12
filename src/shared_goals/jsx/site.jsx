'use strict'

import Goal from 'goal'
import Suggestion from 'suggestion'
import React from 'react'
import ReactDOM from 'react-dom'

var Site = React.createClass({
  render: function() {}
});

Site.Home = (props) =>
  <div className="container">
    <div className="text-center">
      <h1>Shared Goals</h1>
    </div>
    <Goal.CardListBox />
  </div>

Site.Goal = (props) =>
  <div className="container">
    <div className="text-center">
      <h1>Your goal...</h1>
    </div>
    <Suggestion.CardGridBox url="api/suggestions/{this.props.goal_slug}" />
  </div>

export default Site