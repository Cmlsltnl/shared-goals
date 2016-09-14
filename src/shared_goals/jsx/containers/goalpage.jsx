'use strict'

import Goal from 'presentation/goal'
import Suggestion from 'presentation/suggestion'
import React from 'react'
import ReactDOM from 'react-dom'
import { connect } from 'react-redux'
import Actions from 'actions'

var GoalPage = React.createClass({
  render: function() {}
});


GoalPage.Page = React.createClass({
  componentDidMount: function() {
    this.props.fetchGoal(this.props.params.goal_slug);
    this.props.fetchSuggestionsIfNeeded(this.props.params.goal_slug);
  },

  render: function() {
    return (
      <div className="container">
        <Goal.PageHeader goal={this.props.goal} />
        <Suggestion.CardGrid
          goal_slug={this.props.params.goal_slug}
          suggestions={this.props.suggestions}
        />
      </div>
    );
  }
});

GoalPage.Page = connect(
  function(state) {
    return {
      goal: state.goal.json,
      suggestions: state.suggestions.json
    }
  },

  function(dispatch) {
    return {
      fetchGoal: (goal_slug) => {
        dispatch(Actions.fetchGoal(goal_slug))
      },
      fetchSuggestionsIfNeeded: (goal_slug) => {
        dispatch(Actions.fetchSuggestionsIfNeeded(goal_slug))
      }
    }
  }
)(GoalPage.Page)

export default GoalPage
