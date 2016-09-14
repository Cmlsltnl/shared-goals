import { combineReducers } from 'redux'

let initialGoal = {
  title: "",
  pk: -1,
  slug: ""
}

const goalReducer = (state = initialGoal, action) => {
  return state;
}

const suggestionsReducer = (state = [], action) => {
  return state;
}

const goalsReducer = (state = [], action) => {
  return state;
}

const appReducer = combineReducers({
  goal: goalReducer,
  suggestions: suggestionsReducer,
  goals: goalsReducer,
})

export default appReducer