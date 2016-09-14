'use strict'

import React, { PropTypes } from 'react'

var Review = React.createClass({
  render: function() {}
});

Review.Form = React.createClass({
  componentDidMount: function() {
    $("#rateit-review").rateit();
  },

  render: function() {
    let goal = this.props.goal;
    let suggestion = this.props.suggestion;
    let is_action = suggestion.get_type_display === 'action';

    return (
      <div className="row" id="review--form">
        <div className="col-md-8 col-md-offset-2">
          <label className="form--label">Rate this suggestion and give feedback</label>
          <div
            id="rateit-review"
            data_rateit_resetable="false"
          />
          <p>
            <label class="form--label">
              {
                "Do you have any experience with the suggested "
                + suggestion.get_type_display + "?"
              }
            </label>
            <p>
              <select id="id_experience" name="experience">
                <option value="0" selected="selected">I've not tried this</option>
                <option value="1">Yes, I've tried this myself</option>
                <option value="2" disabled={is_action} hidden={is_action}>I've tried this, and I'm still doing it</option>
              </select>
            </p>
          </p>
          <textarea rows={10} className="review--form--text" />
        </div>
      </div>
    )
  }
});

export default Review
