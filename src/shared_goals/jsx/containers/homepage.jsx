'use strict'

import Actions from 'actions'
import Goal from 'presentation/goal'

import React from 'react'
import ReactDOM from 'react-dom'
import { connect } from 'react-redux'

var HomePage = React.createClass({
  render: function() {}
});

HomePage.Page = React.createClass({
  componentDidMount: function() {
    this.props.fetchGoalsIfNeeded();
  },

  render: function() {
    return (
      <div className="container">
        <div className="text-center">
          <h1>Shared Goals</h1>
        </div>
        <Goal.CardList goals={this.props.goals} />
      </div>
    )
  }
});

HomePage.Page = connect(
  function(state) {
    return {
      goals: state.goals.json
    }
  },

  function(dispatch) {
    return {
      fetchGoalsIfNeeded: () => {
        dispatch(Actions.fetchGoalsIfNeeded())
      }
    }
  }
)(HomePage.Page)

export default HomePage