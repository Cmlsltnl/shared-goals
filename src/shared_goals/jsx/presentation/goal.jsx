'use strict'

import React, { PropTypes } from 'react'
import { Link, browserHistory } from 'react-router'

var Goal = React.createClass({
  render: function() {}
});

Goal.Card = ({ title, goal_slug }) => (
  <div className="goal row">
    <Link to={ {pathname: "/to/" + goal_slug + "/"} }>
      {title}
    </Link>
  </div>
);

Goal.Card.propTypes = {
  title: PropTypes.string.isRequired,
  goal_slug: PropTypes.string.isRequired
}

Goal.CardList = ({ goals }) => {
  var goalNodes = goals.map(function(goal) {
    return (
      <Goal.Card title={goal.title} goal_slug={goal.slug} key={goal.pk}/>
    );
  });
  return (
    <div className="goalList">
    {goalNodes}
    </div>
  );
}

Goal.CardList.propTypes = {
  goals: PropTypes.array
}

Goal.PageButtonGroup = ({ onClickSuggestions }) => {
  return (
    <div className="button-grp text-center">
      <button
        className="btn btn-default"
        onClick={onClickSuggestions}
      >
        Suggestions
      </button>
      <button className="btn btn-default">Members</button>
    </div>
  );
}

Goal.PageTitle = ({ goal }) => {
  return (
    <div className="text-center">
      <h1>{goal.title}</h1>
    </div>
  );
}

Goal.PageHeader = ({ goal }) => {
  return (
    <span>
      <Goal.PageTitle goal={goal}/>
      <Goal.PageButtonGroup
        goal={goal}
        onClickSuggestions={
          () => {browserHistory.push('/to/' + goal.slug + "/")}
        }
      />
    </span>
  );
}

export default Goal
