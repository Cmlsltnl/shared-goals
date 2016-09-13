'use strict'

import Goal from 'goal'
import Suggestion from 'suggestion'
import React from 'react'
import ReactDOM from 'react-dom'

var GoalPage = React.createClass({
  render: function() {}
});

GoalPage.ButtonGroup = React.createClass({
  render: function() {
    return (
      <div className="button-grp text-center">
        <button className="btn btn-default">Suggestions</button>
        <button className="btn btn-default">Members</button>
      </div>
    );
  }
});

GoalPage.Title = React.createClass({
  render: function() {
    return (
      <div className="text-center">
        <h1>{this.props.goal.title}</h1>
      </div>
    );
  }
});

GoalPage.Header = React.createClass({
  render: function() {
    return (
      <span>
        <GoalPage.Title goal={this.props.goal}/>
        <GoalPage.ButtonGroup goal={this.props.goal}/>
      </span>
    );
  }
});

GoalPage.HeaderBox = React.createClass({
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
      <GoalPage.Header goal={this.state.goal} />
    );
  }
});

GoalPage.Page = React.createClass({
  render: function() {
    return (
      <div className="container">
        <GoalPage.HeaderBox goal_slug={this.props.params.goal_slug} />
        <Suggestion.CardGridBox goal_slug={this.props.params.goal_slug} />
      </div>
    );
  }
});

export default GoalPage