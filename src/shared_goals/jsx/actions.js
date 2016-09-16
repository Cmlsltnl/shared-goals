import React from 'react'
import fetch from 'isomorphic-fetch'

var Actions = React.createClass({
  render: function() {}
});

export const REQUEST_BUNDLE = 'REQUEST_BUNDLE'
export const RECEIVE_BUNDLE = 'RECEIVE_BUNDLE'
export const REQUEST_GOALS = 'REQUEST_GOALS'
export const RECEIVE_GOALS = 'RECEIVE_GOALS'
export const REQUEST_SUGGESTIONS = 'REQUEST_SUGGESTIONS'
export const RECEIVE_SUGGESTIONS = 'RECEIVE_SUGGESTIONS'
export const RECEIVE_POSTED_GOAL = 'RECEIVE_POSTED_GOAL'
export const RECEIVE_POSTED_SUGGESTION = 'RECEIVE_POSTED_SUGGESTION'
export const RECEIVE_POSTED_REVIEW = 'RECEIVE_POSTED_REVIEW'
export const SET_SUGGESTION_IMAGE_URL = 'SET_SUGGESTION_IMAGE_URL'
export const SET_NEW_SUGGESTION_IMAGE_URL = 'SET_NEW_SUGGESTION_IMAGE_URL'

function requestBundle() {
  return {
    type: REQUEST_BUNDLE
  }
}

function receiveBundle(json) {
  return {
    type: RECEIVE_BUNDLE,
    json: json
  }
}

Actions.fetchBundle = function(goal_slug="none", suggestion_slug="none") {
  return dispatch => {
    dispatch(requestBundle())
    return fetch(
        '/api/bundle/' + goal_slug + "/" + suggestion_slug,
        {
            credentials: 'same-origin'
        }
    )
      .then(response => response.json())
      .then(json => dispatch(receiveBundle(json)))
  }
}

function requestGoals() {
  return {
    type: REQUEST_GOALS
  }
}

function receiveGoals(json) {
  return {
    type: RECEIVE_GOALS,
    json: json
  }
}

function fetchGoals() {
  return dispatch => {
    dispatch(requestGoals())
    return fetch(
        '/api/goals',
        {
            credentials: 'same-origin'
        }
    )
      .then(response => response.json())
      .then(json => dispatch(receiveGoals(json)))
  }
}

function shouldFetchGoals(state) {
  if (state.goals.isFetching) {
    return false
  } else {
    return true
  }
}

Actions.fetchGoalsIfNeeded = function() {
  return (dispatch, getState) => {
    if (shouldFetchGoals(getState())) {
      return dispatch(fetchGoals())
    }
  }
}

function requestSuggestions(goal_slug) {
  return {
    type: REQUEST_SUGGESTIONS,
    goal_slug: goal_slug
  }
}

function receiveSuggestions(json, goal_slug) {
  return {
    type: RECEIVE_SUGGESTIONS,
    json: json,
    goal_slug: goal_slug
  }
}

function fetchSuggestions(goal_slug) {
  return dispatch => {
    dispatch(requestSuggestions(goal_slug))
    return fetch(
        '/api/suggestions/' + goal_slug,
        {
            credentials: 'same-origin'
        }
    )
      .then(response => response.json())
      .then(json => dispatch(receiveSuggestions(json, goal_slug)))
  }
}

function shouldFetchSuggestions(state, goal_slug) {
  if (state.suggestions.goal_slug !== goal_slug) {
    return true;
  }
  return !state.suggestions.isFetching;
}

Actions.fetchSuggestionsIfNeeded = function(goal_slug) {
  return (dispatch, getState) => {
    if (shouldFetchSuggestions(getState(), goal_slug)) {
      return dispatch(fetchSuggestions(goal_slug))
    }
  }
}

Actions.receivePostedGoal = function(json) {
  return {
  type: RECEIVE_POSTED_GOAL,
    json: json
  }
}

Actions.receivePostedSuggestion = function(json) {
  return {
  type: RECEIVE_POSTED_SUGGESTION,
    json: json
  }
}

Actions.receivePostedReview = function(json) {
  return {
  type: RECEIVE_POSTED_REVIEW,
    json: json
  }
}

Actions.fetchBundle = function(goal_slug="none", suggestion_slug="none") {
  return dispatch => {
    dispatch(requestBundle())
    return fetch(
        '/api/bundle/' + goal_slug + "/" + suggestion_slug,
        {
            credentials: 'same-origin'
        }
    )
      .then(response => response.json())
      .then(json => dispatch(receiveBundle(json)))
  }
}

Actions.setSuggestionImageUrl = function(url) {
  return {
  type: SET_SUGGESTION_IMAGE_URL,
    url: url
  }
}

Actions.setNewSuggestionImageUrl = function(url) {
  return {
  type: SET_NEW_SUGGESTION_IMAGE_URL,
    url: url
  }
}


export default Actions
