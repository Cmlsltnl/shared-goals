'use strict'

import Goal from 'goal'
import React from 'react'
import ReactDOM from 'react-dom'

var Home = React.createClass({
  render: function() {}
});

Home.Home = (props) =>
  <div className="container">
    <div className="text-center">
      <h1>Shared Goals</h1>
    </div>
    <Goal.CardListBox />
  </div>

export default Home