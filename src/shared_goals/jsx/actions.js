import React from 'react'
import fetch from 'isomorphic-fetch'

var Actions = React.createClass({
  render: function() {}
});

export const REQUEST_GOAL = 'REQUEST_GOAL'
export const RECEIVE_GOAL = 'RECEIVE_GOAL'
export const REQUEST_GOALS = 'REQUEST_GOALS'
export const RECEIVE_GOALS = 'RECEIVE_GOALS'
export const REQUEST_SUGGESTIONS = 'REQUEST_SUGGESTIONS'
export const RECEIVE_SUGGESTIONS = 'RECEIVE_SUGGESTIONS'
export const REQUEST_SUGGESTION = 'REQUEST_SUGGESTION'
export const RECEIVE_SUGGESTION = 'RECEIVE_SUGGESTION'

function requestGoal() {
  return {
    type: REQUEST_GOAL
  }
}

function receiveGoal(json) {
  return {
    type: RECEIVE_GOAL,
    json: json
  }
}

Actions.fetchGoal = function(goal_slug) {
  return dispatch => {
    dispatch(requestGoal())
    return fetch('/api/goal/' + goal_slug)
      .then(response => response.json())
      .then(json => dispatch(receiveGoal(json)))
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
    return fetch('/api/goals')
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
    return fetch('/api/suggestions/' + goal_slug)
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

function requestSuggestion() {
  return {
    type: REQUEST_SUGGESTION
  }
}

function receiveSuggestion(json) {
  return {
    type: RECEIVE_SUGGESTION,
    json: json
  }
}

Actions.fetchSuggestion = function(goal_slug, suggestion_slug) {
  return dispatch => {
    dispatch(requestSuggestion())
    return fetch('/api/suggestion/' + goal_slug + "/" + suggestion_slug)
      .then(response => response.json())
      .then(json => dispatch(receiveSuggestion(json)))
  }
}

export default Actions
