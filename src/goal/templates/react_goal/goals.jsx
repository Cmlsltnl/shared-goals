{% extends 'react_base.html' %}
{% block react %}

var Goal = React.createClass({
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

var GoalList = React.createClass({
  render: function() {
    var goalNodes = this.props.data.map(function(goal) {
      return (
        <Goal goal={goal} key={goal.pk}/>
      );
    });
    return (
      <div className="goalList">
      {goalNodes}
      </div>
    );
  }
});

var GoalsBox = React.createClass({
  loadGoalsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
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
        <h1>Goals</h1>
        <GoalList data={this.state.data} />
      </div>
    );
  }
});

ReactDOM.render(
  <GoalsBox url="/api/goals" pollInterval={100000} />,
  document.getElementById('content')
);

{% endblock %}
