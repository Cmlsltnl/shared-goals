'use strict'

import Actions from 'actions'
import GoalPage from 'containers/goalpage'
import Goal from 'presentation/goal'
import Review from 'presentation/review'
import Suggestion from 'presentation/suggestion'

import React from 'react'
import ReactDOM from 'react-dom'
import { connect } from 'react-redux'

var SuggestionPage = React.createClass({
  render: function() {}
});

SuggestionPage.Page = React.createClass({
  componentDidMount: function() {
    this.props.fetchGoal(this.props.params.goal_slug)
    this.props.fetchSuggestion(
      this.props.params.goal_slug, this.props.params.suggestion_slug
    )
  },

  render: function() {
    let goal = this.props.goal;
    let suggestion = this.props.suggestion;

    return (
      <div className="container">
        <Goal.PageHeader goal={goal} />
        <Suggestion.PageHeader
          url={"/to/" + goal.slug + "/by/" + suggestion.slug + "/"}
          suggestion={suggestion}
          revision={suggestion.current_revision}
        />
        <Review.Form
          goal={goal}
          suggestion={suggestion}
        />
      </div>
    );
  }
});

SuggestionPage.Page = connect(
  function(state) {
    return {
      goal: state.goal.json,
      suggestion: state.suggestion.json
    }
  },

  function(dispatch) {
    return {
      fetchGoal: (goal_slug) => {
        dispatch(Actions.fetchGoal(goal_slug))
      },
      fetchSuggestion: (goal_slug, suggestion_slug) => {
        dispatch(Actions.fetchSuggestion(goal_slug, suggestion_slug))
      }
    }
  }
)(SuggestionPage.Page);

export default SuggestionPage
