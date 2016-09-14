'use strict'

import React, { PropTypes } from 'react'
import { Link } from 'react-router'

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

Goal.CardListBox = React.createClass({
  loadGoalsFromServer: function() {
    $.ajax({
      url: "api/goals",
      dataType: 'json',
      cache: false,
      success: function(data) { this.setState({data: data}); }.bind(this),
      error: function(xhr, status, err) { console.error("api/goals", status, err.toString()); }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadGoalsFromServer();
    setInterval(this.loadGoalsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="goalsBox">
        <Goal.CardList goals={this.state.data} />
      </div>
    );
  }
});

export default Goal
