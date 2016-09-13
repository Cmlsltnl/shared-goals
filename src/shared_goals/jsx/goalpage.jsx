'use strict'

import Goal from 'goal'
import Suggestion from 'suggestion'
import React from 'react'
import ReactDOM from 'react-dom'

var GoalPage = React.createClass({
  render: function() {}
});

GoalPage.Header = React.createClass({
  url: function() { return "/api/goal/" + this.props.goal_slug; },
  loadGoalFromServer: function() {
    $.ajax({
      url: this.url(),
      dataType: 'json',
      cache: false,
      success: function(data) { this.setState({goal: data}); }.bind(this),
      error: function(xhr, status, err) { console.error(this.url(), status, err.toString()); }.bind(this)
    });
  },
  getInitialState: function() { return {goal: {}}; },
  componentDidMount: function() { this.loadGoalFromServer(); },
  render: function() {
    return (
      <div className="text-center">
        <h1>{this.state.goal.title}</h1>
      </div>
    );
  }
});

GoalPage.Page = React.createClass({
  render: function() {
    return (
      <div className="container">
        <GoalPage.Header goal_slug={this.props.params.goal_slug} />
        <Suggestion.CardGridBox goal_slug={this.props.params.goal_slug} />
      </div>
    );
  }
});

export default GoalPage