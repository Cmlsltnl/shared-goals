import Widgets from 'presentation/widgets'
import React, { PropTypes } from 'react'
import { Link, browserHistory } from 'react-router'

var Goal = React.createClass({
  render: function() {}
});

Goal.Card = ({ title, goal_slug }) => (
  <div className="goal row">
    <div className="col-md-12">
      <Link to={ {pathname: "/to/" + goal_slug + "/"} }>
        {title}
      </Link>
    </div>
  </div>
);

Goal.Card.propTypes = {
  title: PropTypes.string.isRequired,
  goal_slug: PropTypes.string.isRequired
}

Goal.CardList = ({ goals }) => {
  var goalNodes = goals.map(function(goal) {
    return (
      <Goal.Card title={goal.title} goal_slug={goal.slug} key={goal.id}/>
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

Goal.Form = ({ postGoal, cancelGoal, errors }) => {
  let doPost = function(e)
  {
    e.preventDefault();
    postGoal($("#id_new_goal_form").serialize());
  }.bind(this);

  let doCancel = function(e)
  {
    e.preventDefault();
    cancelGoal();
  }.bind(this);

  return (
    <form id="id_new_goal_form">
      <p>
        <label className="form--label">Title</label>
        <input id="id_title" maxLength="100" name="title" type="text" defaultValue=""/>
        <Widgets.errorLabel errors={errors} fieldName="title" />
      </p>
      <div>
        <div className="gap--small-above gap--small-below">
          <label className="form--label">All done, press Submit to publish your goal</label>
          <button name="submit" value="save" onClick={doPost}>Submit</button>
          <button name="submit" value="cancel" onClick={doCancel}>Cancel</button>
        </div>
      </div>
    </form>
  );
}

export default Goal
