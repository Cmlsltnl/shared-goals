'use strict'

var React = require('react')

var Goal = React.createClass({
  render: function() {}
});


Goal.Card = React.createClass({
  render: function() {
    return (
      <div className="goal row">
        <a href={this.props.goal.get_url}>
          {this.props.goal.title}
        </a>
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
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error("api/goals", status, err.toString());
      }.bind(this)
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

Goal.Homer2 = (props) =>
  <div className="container">
    <div className="text-center">
      <h1>Shared Goals</h1>
    </div>
    <Goal.CardListBox />
  </div>

export default Goal
