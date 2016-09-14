import { combineReducers } from 'redux'
import
  Actions,
  {
     REQUEST_GOAL,
     RECEIVE_GOAL,
     REQUEST_GOALS,
     RECEIVE_GOALS,
     REQUEST_SUGGESTION,
     RECEIVE_SUGGESTION,
     REQUEST_SUGGESTIONS,
     RECEIVE_SUGGESTIONS
  } from 'actions'

function goalReducer(
  state = {
    json: {
      title: "",
      pk: -1,
      slug: ""
    },
    isFetching: false
  },
  action
)
{
  switch (action.type) {
    case REQUEST_GOAL:
      return Object.assign({}, state, {
        isFetching: true
      })
    case RECEIVE_GOAL:
      return Object.assign({}, state, {
        json: action.json,
        isFetching: false
      })
    default:
      return state
  }
}

function suggestionReducer(
  state = {
    json: {
      owner: {
        name: ""
      },
      pub_date_display: "",
      current_revision: {
        description: ""
      }
    },
    isFetching: false
  },
  action
)
{
  switch (action.type) {
    case REQUEST_SUGGESTION:
      return Object.assign({}, state, {
        isFetching: true
      })
    case RECEIVE_SUGGESTION:
      return Object.assign({}, state, {
        json: action.json,
        isFetching: false
      })
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

const appReducer = combineReducers({
  goal: goalReducer,
  goals: goalsReducer,
  suggestion: suggestionReducer,
  suggestions: suggestionsReducer
})

export default appReducer