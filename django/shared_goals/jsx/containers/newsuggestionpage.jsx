import React from 'react'
import { connect } from 'react-redux'

import Actions from 'actions'
import Goal from 'presentation/goal'
import Suggestion from 'presentation/suggestion'
import SuggestionPageMixin from 'containers/suggestionpagemixin'


var NewSuggestionPage = React.createClass({
  render: function() {}
});

NewSuggestionPage.Page = React.createClass({
  mixins: [SuggestionPageMixin],

  componentDidMount: function() {
    this.props.fetchBundle(this.props.params.goal_slug);
  },

  getImageUploadUrl: function() {
    return (
      '/api/upload-suggestion-image/' + this.props.params.goal_slug
    );
  },

  getSuggestionUrl: function() {
    return (
      '/api/new-suggestion/' + this.props.params.goal_slug
    );
  },

  postNewSuggestion: function(form_data) {
    this.postSuggestion(
      form_data,
      function(data) {
        return "/to/" + this.props.params.goal_slug + "/by/" + data.suggestion_slug + "/"
      }.bind(this)
    );
  },

  postNewSuggestionDraft: function(form_data)
  {
    this.postSuggestion(
      form_data,
      function(data) {
        return "/to/" + this.props.params.goal_slug + "/"
      }.bind(this)
    );
  },

  render: function() {
    if (!this.props.goal)
    {
      return (<div/>);
    }

    return (
      <div className="container">
        <div className="row">
          <div className="col-md-8 col-md-offset-2">
            <Goal.PageHeader goal={this.props.goal} />
            <h1>New suggestion</h1>
            <Suggestion.Form
              suggestion={this.props.newSuggestion}
              uploadImage={this.uploadImage}
              postSuggestion={this.postNewSuggestion}
              cancelPostSuggestion={this.postNewSuggestionDraft}
              errors={this.props.suggestionPostResult.errors}
            />
          </div>
        </div>
      </div>
    );
  }
});

NewSuggestionPage.Page = connect(
  function(state) {
    return {
      suggestionPostResult: state.postResults.suggestion,
      newSuggestion: state.bundle.newSuggestion,
      goal: state.bundle.goal,
    }
  },

  function(dispatch) {
    return {
      fetchBundle: (goal_slug) => {
        dispatch(Actions.fetchBundle(goal_slug))
      },
      receivePostedSuggestion: (json) => {
        dispatch(Actions.receivePostedSuggestion(json))
      },
      setImageUrl: (url) => {
        dispatch(Actions.setNewSuggestionImageUrl(url))
      },
    }
  }
)(NewSuggestionPage.Page)

export default NewSuggestionPage
