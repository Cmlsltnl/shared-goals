import Goal from 'presentation/goal'
import React from 'react'
import { connect } from 'react-redux'
import { browserHistory } from 'react-router'
import Actions from 'actions'

var NewGoalPage = React.createClass({
  render: function() {}
});

NewGoalPage.Page = React.createClass({
  componentDidMount: function() {
    this.props.fetchBundle();
  },

  postGoal: function(form_data) {
    $.ajax({
      type: "POST",
      url: '/api/new-goal',
      data: form_data,
      success: function(data)
      {
        this.props.receivePostedGoal(data);
        if (data.success) {
          browserHistory.push("/to/" + data.goal_slug + "/")
        }
      }.bind(this)
    });
  },

  cancelGoal: function()
  {
    browserHistory.push('/')
  },

  render: function() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-8 col-md-offset-2">
            <h1>New goal</h1>
            <Goal.Form
              postGoal={this.postGoal}
              cancelGoal={this.cancelGoal}
              errors={this.props.goalPostResult.errors}
            />
          </div>
        </div>
      </div>
    );
  }
});

NewGoalPage.Page = connect(
  function(state) {
    return {
      goalPostResult: state.postResults.goal
    }
  },

  function(dispatch) {
    return {
      fetchBundle: (goal_slug) => {
        dispatch(Actions.fetchBundle(goal_slug))
      },
      receivePostedGoal: (json) => {
        dispatch(Actions.receivePostedGoal(json))
      },
    }
  }
)(NewGoalPage.Page)

export default NewGoalPage
