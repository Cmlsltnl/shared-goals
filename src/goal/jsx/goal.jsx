'use strict'

import React from 'react'
import { Link } from 'react-router'

var Goal = React.createClass({
  render: function() {}
});


Goal.Card = React.createClass({
  render: function() {
    return (
      <div className="goal row">
        <Link to={ {pathname: "/to/become-a-yogi/"} }>
          {this.props.goal.title}
        </Link>
      </div>
    );
  }
});

Goal.CardList = React.createClass({
  render: function() {
    var goalNodes = this.props.data.map(function(goal) {
      return (
        <Goal.Card goal={goal} key={goal.pk}/>
      );
    });
    return (
      <div className="goalList">
      {goalNodes}
      </div>
    );
  }
});

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
        <Goal.CardList data={this.state.data} />
      </div>
    );
  }
});

export default Goal
