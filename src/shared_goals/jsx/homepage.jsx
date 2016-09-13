'use strict'

import Goal from 'goal'

import React from 'react'
import ReactDOM from 'react-dom'

var HomePage = React.createClass({
  render: function() {}
});

HomePage.Page = (props) =>
  <div className="container">
    <div className="text-center">
      <h1>Shared Goals</h1>
    </div>
    <Goal.CardListBox />
  </div>

export default HomePage