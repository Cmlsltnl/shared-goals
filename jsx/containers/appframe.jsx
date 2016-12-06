import TopBar from 'presentation/topbar'

import React from 'react'
import ReactDOM from 'react-dom'
import { connect } from 'react-redux'
import { browserHistory } from 'react-router'

var AppFrame = React.createClass({
  render: function() {}
});

AppFrame.Frame = React.createClass({
  onNewGoal: function() {
    browserHistory.push('/new-goal/')
  },

  onNewSuggestion: function() {
    browserHistory.push('/to/' + this.props.goal.slug + '/new-suggestion/')
  },

  onEditSuggestion: function() {
    browserHistory.push(
      '/to/' + this.props.goal.slug + '/by/' + this.props.suggestion.slug + '/edit-suggestion/'
    )
  },

  render: function() {
    return (
      <span>
        <div className="container">
          <TopBar.Bar
            flags={this.props.flags}
            onNewGoal={this.onNewGoal}
            onNewSuggestion={this.onNewSuggestion}
            onEditSuggestion={this.props.suggestion ? this.onEditSuggestion : null}
          />
        </div>
        {this.props.children}
      </span>
    );
  }
});

AppFrame.Frame = connect(
  function(state) {
    return {
      flags: state.bundle.flags,
      goal: state.bundle.goal,
      suggestion: state.bundle.suggestion,
    }
  }
)(AppFrame.Frame);

export default AppFrame