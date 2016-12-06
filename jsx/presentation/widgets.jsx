import React, { PropTypes } from 'react'


var Widgets = React.createClass({
  render: function() {}
});

Widgets.errorLabel = ({ errors, fieldName }) => {
  return (
    errors && errors[fieldName]
      ? (<h5 className="form--error">{errors[fieldName]}</h5>)
      : null
  );
}

export default Widgets;
