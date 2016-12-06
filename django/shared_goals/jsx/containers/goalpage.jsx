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
    this.props.fetchBundle(this.props.params.goal_slug);
    this.props.fetchSuggestionsIfNeeded(this.props.params.goal_slug);
  },

  render: function() {
    let goal = this.props.goal;
    let suggestions = this.props.suggestions;

    if (!goal || !suggestions)
    {
      return (<div/>);
    }

    return (
      <div className="container">
        <Goal.PageHeader goal={goal} />
        <Suggestion.CardGrid
          goal_slug={goal.slug}
          suggestions={suggestions}
        />
      </div>
    );
  }
});

GoalPage.Page = connect(
  function(state) {
    return {
      goal: state.bundle.goal,
      suggestions: state.suggestions.json
    }
  },

  function(dispatch) {
    return {
      fetchBundle: (goal_slug) => {
        dispatch(Actions.fetchBundle(goal_slug))
      },
      fetchSuggestionsIfNeeded: (goal_slug) => {
        dispatch(Actions.fetchSuggestionsIfNeeded(goal_slug))
      }
    }
  }
)(GoalPage.Page)

export default GoalPage
