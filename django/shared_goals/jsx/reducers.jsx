import { combineReducers } from 'redux'
import
  Actions,
  {
    REQUEST_BUNDLE,
    RECEIVE_BUNDLE,
    REQUEST_GOALS,
    RECEIVE_GOALS,
    REQUEST_SUGGESTIONS,
    RECEIVE_SUGGESTIONS,
    RECEIVE_POSTED_GOAL,
    RECEIVE_POSTED_SUGGESTION,
    RECEIVE_POSTED_REVIEW,
    SET_SUGGESTION_IMAGE_URL,
    SET_NEW_SUGGESTION_IMAGE_URL,
  } from 'actions'

function bundleReducer(
  state = {
    json: {},
    isFetching: false
  },
  action
)
{
  switch (action.type) {
    case REQUEST_BUNDLE:
      return Object.assign({}, state, {
        isFetching: true
      })
    case RECEIVE_BUNDLE:
      return Object.assign({}, state, {
        goal: action.json.goal,
        suggestion: action.json.suggestion,
        newSuggestion: action.json.new_suggestion,
        review: action.json.review,
        flags: action.json.flags,
        isFetching: false
      })
    case SET_NEW_SUGGESTION_IMAGE_URL:
      let newSuggestion = Object.assign({}, state.newSuggestion, {
        uncropped_image: action.url
      });
      return Object.assign({}, state, {
        newSuggestion: newSuggestion
      });
    case SET_SUGGESTION_IMAGE_URL:
      let suggestion = Object.assign({}, state.suggestion, {
        uncropped_image: action.url
      });
      return Object.assign({}, state, {
        suggestion: suggestion
      });
    default:
      return state
  }
}

function suggestionsReducer(
  state = {
    json: [],
    isFetching: false,
    goal_slug: ""
  },
  action
)
{
  switch (action.type) {
    case REQUEST_SUGGESTIONS:
      return Object.assign({}, state, {
        isFetching: true,
        goal_slug: action.goal_slug
      })
    case RECEIVE_SUGGESTIONS:
      return Object.assign({}, state, {
        json: action.json,
        isFetching: false,
        goal_slug: action.goal_slug
      })
    default:
      return state
  }
}

function goalsReducer(
  state = {
    json: [],
    isFetching: false
  },
  action
)
{
  switch (action.type) {
    case REQUEST_GOALS:
      return Object.assign({}, state, {
        isFetching: true
      })
    case RECEIVE_GOALS:
      return Object.assign({}, state, {
        json: action.json,
        isFetching: false
      })
    default:
      return state
  }
}

function postResultsReducer(
  state = {
    goal: {},
    suggestion: {},
    review: {},
  },
  action
)
{
  switch (action.type) {
    case RECEIVE_POSTED_GOAL:
      return Object.assign({}, state, {
        goal: action.json
      })
    case RECEIVE_POSTED_SUGGESTION:
      return Object.assign({}, state, {
        suggestion: action.json
      })
    case RECEIVE_POSTED_REVIEW:
      return Object.assign({}, state, {
        review: action.json
      })
    default:
      return state
  }
}

const appReducer = combineReducers({
  bundle: bundleReducer,
  goals: goalsReducer,
  suggestions: suggestionsReducer,
  postResults: postResultsReducer,
})

export default appReducer
