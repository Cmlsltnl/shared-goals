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
    this.props.fetchBundle();
    this.props.fetchGoalsIfNeeded();
  },

  render: function() {
    let goals = this.props.goals;
    if (!goals)
    {
      return (<div/>);
    }

    return (
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <div className="text-center">
              <h1>Shared Goals</h1>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <Goal.CardList goals={goals} />
          </div>
        </div>
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
      fetchBundle: () => {
        dispatch(Actions.fetchBundle())
      },
      fetchGoalsIfNeeded: () => {
        dispatch(Actions.fetchGoalsIfNeeded())
      }
    }
  }
)(HomePage.Page)

export default HomePage