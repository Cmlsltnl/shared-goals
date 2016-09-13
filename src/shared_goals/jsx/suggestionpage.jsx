'use strict'

import Goal from 'goal'
import GoalPage from 'goalpage'
import Suggestion from 'suggestion'
import React from 'react'
import ReactDOM from 'react-dom'

var SuggestionPage = React.createClass({
  render: function() {}
});

SuggestionPage.Header = React.createClass({
  render: function() {
    return (
      <div class="row gap--small-below">
        <div class="col-md-2"></div>
        <div class="col-md-8">
          <h5>Published by {this.props.suggestion.owner.name}, this.props.suggestion.pub_date</h5>
          this.props.suggestion.current_revision.description
        </div>
      </div>
    );
  }
});

SuggestionPage.SuggestionBox = React.createClass({
  url: function() {
    return "/api/suggestion/" + this.props.goal_slug + "/" + this.props.suggestion_slug;
  },
  loadFromServer: function() {
    $.ajax({
      url: this.url(),
      dataType: 'json',
      cache: false,
      success: function(data) { this.setState({suggestion: data}); }.bind(this),
      error: function(xhr, status, err) { console.error(this.url(), status, err.toString()); }.bind(this)
    });
  },
  getInitialState: function() {
    return {
        suggestion: {
            goal: {}
        }
    };
  },
  componentDidMount: function() { this.loadFromServer(); },
  render: function() {
    return (
      <span>
          <GoalPage.Header goal={this.state.suggestion.goal} />
          <SuggestionPage.Header suggestion={this.state.suggestion} />
      </span>
    );
  }
});

SuggestionPage.Page = React.createClass({
  render: function() {
    return (
      <div className="container">
        <SuggestionPage.SuggestionBox
          goal_slug={this.props.params.goal_slug}
          suggestion_slug={this.props.params.suggestion_slug}
        />
      </div>
    );
  }
});

export default SuggestionPage
