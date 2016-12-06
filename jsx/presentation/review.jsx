'use strict'

import React, { PropTypes } from 'react'

var Review = React.createClass({
  render: function() {}
});

Review.Form = React.createClass({
  componentDidMount: function() {
    $("#rateit-review").rateit();
    $('#rateit-review').bind('rated', function() {
        $('#id_rating').val($(this).rateit('value'));
    });
  },

  doPost: function(e)
  {
    e.preventDefault();
    this.props.postReview($("#id_review_form").serialize());
  },

  doCancel: function(e)
  {
    e.preventDefault();
    this.refs.reviewForm.reset();
    $('#rateit-review').rateit('value', this.review_rating());
    $('#id_experience').val(this.review_experience());
  },

  review_rating: function()
  {
    return this.props.review
      ? this.props.review.rating.toString()
      : "0";
  },

  review_experience: function()
  {
    return this.props.review
      ? this.props.review.experience
      : 0;
  },

  review_text: function()
  {
    return this.props.review
      ? this.props.review.description
      : "";
  },

  render: function() {
    let goal = this.props.goal;
    let suggestion = this.props.suggestion;
    let review = this.props.review;

    if (!goal || !suggestion)
    {
      return (<div/>);
    }

    let header_label = review
      ? "Update your review of this suggestion"
      : "Rate this suggestion and give feedback";
    let is_action = suggestion.type_display === 'action';

    return (
      <div className="row" id="review--form">
        <div className="col-md-8 col-md-offset-2">
          <form id="id_review_form" ref="reviewForm">
            <label className="form--label"></label>
            <input
              id="id_rating"
              type="hidden"
              name="rating"
              value={this.review_rating()}
            />
            <div
              id="rateit-review"
              data-rateit-resetable="false"
              data-rateit-value={this.review_rating()}
            />
            <p><label class="form--label">{header_label}</label></p>
            <p>
              <select id="id_experience" name="experience" defaultValue={this.review_experience()}>
                <option value="0">I've not tried this</option>
                <option value="1">Yes, I've tried this myself</option>
                <option value="2" disabled={is_action} hidden={is_action}>I've tried this, and I'm still doing it</option>
              </select>
            </p>
            <textarea
              id="id_review_description"
              name="description"
              rows={10}
              className="review--form--text"
              defaultValue={this.review_text()}
            />
            <div>
              <button name="submit" value="save" onClick={this.doPost}>Submit</button>
              <button name="submit" value="cancel" onClick={this.doCancel}>Cancel</button>
            </div>
          </form>
        </div>
      </div>
    )
  }
});

export default Review
