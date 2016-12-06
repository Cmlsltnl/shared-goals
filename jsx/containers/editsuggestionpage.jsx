import React from 'react'
import { connect } from 'react-redux'
import { browserHistory } from 'react-router'

import Actions from 'actions'
import Suggestion from 'presentation/suggestion'
import Goal from 'presentation/goal'
import SuggestionPageMixin from 'containers/suggestionpagemixin'


var EditSuggestionPage = React.createClass({
  render: function() {}
});

EditSuggestionPage.Page = React.createClass({
  mixins: [SuggestionPageMixin],

  componentDidMount: function() {
    this.props.fetchBundle(
      this.props.params.goal_slug,
      this.props.params.suggestion_slug,
    );
  },

  getImageUploadUrl: function() {
    return (
      '/api/upload-suggestion-image/' + this.props.params.goal_slug
      + '/' + this.props.params.suggestion_slug
    );
  },

  getSuggestionUrl: function() {
    return (
      '/api/edit-suggestion/' + this.props.params.goal_slug
      + '/' + this.props.params.suggestion_slug
    );
  },

  postEditedSuggestion: function(form_data) {
    this.postSuggestion(
      form_data,
      function(data) {
        return "/to/" + this.props.params.goal_slug + "/by/" + data.suggestion_slug + "/"
      }.bind(this)
    )
  },

  cancelEdit: function(form_data)
  {
    browserHistory.push("/to/" + this.props.params.goal_slug + "/")
  },

  render: function() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-8 col-md-offset-2">
            <Goal.PageHeader goal={this.props.goal} />
            <h1>Edit suggestion</h1>
            <Suggestion.Form
              suggestion={this.props.suggestion}
              uploadImage={this.uploadImage}
              postSuggestion={this.postEditedSuggestion}
              cancelPostSuggestion={this.cancelEdit}
              errors={this.props.suggestionPostResult.errors}
            />
          </div>
        </div>
      </div>
    );
  }
});

EditSuggestionPage.Page = connect(
  function(state) {
    return {
      suggestionPostResult: state.postResults.suggestion,
      suggestion: state.bundle.suggestion,
      goal: state.bundle.goal,
    }
  },

  function(dispatch) {
    return {
      fetchBundle: (goal_slug, suggestion_slug) => {
        dispatch(Actions.fetchBundle(goal_slug, suggestion_slug))
      },
      receivePostedSuggestion: (json) => {
        dispatch(Actions.receivePostedSuggestion(json))
      },
      setImageUrl: (url) => {
        dispatch(Actions.setSuggestionImageUrl(url))
      },
    }
  }
)(EditSuggestionPage.Page)

export default EditSuggestionPage
