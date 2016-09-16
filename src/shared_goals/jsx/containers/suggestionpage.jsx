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
    this.props.fetchBundle(
      this.props.params.goal_slug, this.props.params.suggestion_slug
    )
  },

  render: function() {
    let goal = this.props.goal;
    let suggestion = this.props.suggestion;
    let review = this.props.review;
    let flags = this.props.flags;
    let fetchBundle = this.props.fetchBundle;
    let reportReviewFormErrors = this.props.reportReviewFormErrors;

    if (!goal || !suggestion)
    {
      return (<div/>);
    }

    let postReview = function(form_data) {
      $.ajax({
        type: "POST",
        url: "/api/review/" + goal.slug + "/" + suggestion.slug,
        data: form_data,
        success: function(data)
        {
          this.props.receivePostedReview(data);
        }.bind(this)
      });
    }.bind(this)

    return (
      <div className="container">
        <Goal.PageHeader goal={goal} />
        <Suggestion.PageHeader
          url={"/to/" + goal.slug + "/by/" + suggestion.slug + "/"}
          suggestion={suggestion}
        />
        {
          flags.add_review
          ? <Review.Form goal={goal}
            suggestion={suggestion}
            review={review}
            postReview={postReview}
          />
          : null
        }
      </div>
    );
  }
});

SuggestionPage.Page = connect(
  function(state) {
    return {
      goal: state.bundle.goal,
      suggestion: state.bundle.suggestion,
      review: state.bundle.review,
      flags: state.bundle.flags,
    }
  },

  function(dispatch) {
    return {
      fetchBundle: (goal_slug, suggestion_slug) => {
        dispatch(Actions.fetchBundle(goal_slug, suggestion_slug))
      },
      receivePostedReview: (json) => {
        dispatch(Actions.receivePostedReview(json))
      },
    }
  }
)(SuggestionPage.Page);

export default SuggestionPage
