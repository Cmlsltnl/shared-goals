'use strict'

import React, { PropTypes } from 'react'
import ReactMarkdown from 'react-markdown'

var TopBar = React.createClass({
  render: function() {}
});

TopBar.LinksMenu = ({ }) => {
  let url_home = "/"
  let url_tos = "https://github.com/mnieber/shared-goals/blob/master/TERMS.md"
  let url_about = "https://github.com/mnieber/shared-goals/blob/master/README.md"
  let url_feedback = "https://github.com/mnieber/shared-goals/issues"

  return (
    <span>
      <a href={url_home}>Shared Goals</a>
      <a href={url_about}> | About</a>
      <a href={url_tos}> | Terms</a>
      <a href={url_feedback}> | Give feedback</a>
    </span>
  )
}

TopBar.MemberButtonGroup = ({ flags, onNewGoal, onNewSuggestion, onEditSuggestion }) => {
  let url_update_suggestion = "/"
  let url_new_suggestion = "/"
  let url_new_goal = "/"

  return (
    <div className="btn-group pull-right gap--small-right">
      {
        flags && onEditSuggestion && flags.edit_suggestion
          ? <button className="btn btn-info" onClick={onEditSuggestion}>Edit Suggestion</button>
          : null
      }
      {
        flags && flags.is_member
          ? <button className="btn btn-success" onClick={onNewSuggestion}>New Suggestion</button>
          : null
      }
      {
        flags && flags.add_goal
          ? <button className="btn btn-success" onClick={onNewGoal}>New Goal</button>
          : null
      }
      {
        flags && flags.join_goal
          ? <button className="btn btn-success">Join Goal</button>
          : null
      }
    </div>
  )
}

TopBar.MenuLoggedIn = ({ }) => {
  return (
    <div className="dropdown clearfix pull-right">
      <a className="btn dropdown-toggle" data-toggle="dropdown" href="#">Pete Proxy</a>
      <span className="caret"></span>
      <ul className="dropdown-menu">
        <li>
          <a href="#">Log out</a>
          <a href="#">Change password</a>
        </li>
      </ul>
    </div>
  )
}

TopBar.MenuNotLoggedIn = ({ }) => {
  return (
    <div className="dropdown clearfix pull-right">
      <a href="#">Log in</a>
    </div>
  )
}

TopBar.Bar = ({ flags, onNewGoal, onNewSuggestion, onEditSuggestion }) => {
  return (
    <div className="row gap--tiny-above">
      <div className="col-md-12">
        <TopBar.LinksMenu />
        <TopBar.MenuNotLoggedIn />
        <TopBar.MemberButtonGroup
          flags={flags}
          onNewGoal={onNewGoal}
          onNewSuggestion={onNewSuggestion}
          onEditSuggestion={onEditSuggestion}
        />
      </div>
    </div>
  )
}

export default TopBar
