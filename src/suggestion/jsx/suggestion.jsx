'use strict'

import React, { PropTypes } from 'react'

var Suggestion = React.createClass({
  render: function() {}
});

Suggestion.Card = ({ url, type, stars, title, image }) => {
  var style = {};
  if (image) {
    style.backgroundImage = "url(" + image + ")";
  }

  return (
    <div className="col-md-4">
      <a href={url}>
        <div className="suggestion--image" style={style}>
          <div className="suggestion--gradient"></div>
          <span className="suggestion--title">
            <span className="suggestion--title--caption">
              {type} {stars}
            </span>
            <h3>{title}</h3>
          </span>
        </div>
      </a>
    </div>
  );
}

Suggestion.Card.propTypes = {
  url: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  stars: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  image: PropTypes.string.isRequired,
}

let chunks = function(items, chunkSize) {
    var R = [];
    for (var i=0; i<items.length; i+=chunkSize)
        R.push(items.slice(i,i+chunkSize));
    return R;
}

Suggestion.CardGrid = ({ goal_slug, suggestions }) => {
  var suggestionNodes = suggestions.map(function(suggestion) {
    return (
      <Suggestion.Card
        url={"/to/" + goal_slug + "/by/" + suggestion.slug + "/"}
        type={suggestion.get_type_display}
        stars={suggestion.stars}
        title={suggestion.current_revision.title}
        image={suggestion.image}
        key={suggestion.pk}
      />
    );
  });

  var rows = chunks(suggestionNodes, 3).map(function(chunk, index) {
    return (
      <div className="row gap--small-above" key={index}>
      {chunk}
      </div>
    );
  });

  return (
    <div>
    {rows}
    </div>
  );
}

Suggestion.CardGrid.propTypes = {
  goal_slug: PropTypes.string.isRequired,
  suggestions: PropTypes.array.isRequired
}

Suggestion.CardGridBox = React.createClass({
  url: function() {
    return "/api/suggestions/" + this.props.goal_slug;
  },
  loadSuggestionsFromServer: function() {
    $.ajax({ url: this.url(), dataType: 'json', cache: false,
      success: function(data) { this.setState({data: data}); }.bind(this),
      error: function(xhr, status, err) { console.error(this.url(), status, err.toString()); }.bind(this)
    });
  },
  getInitialState: function() { return {data: []}; },
  componentDidMount: function() {
    this.loadSuggestionsFromServer();
    setInterval(this.loadSuggestionsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="suggestion_CardGridBox">
        <Suggestion.CardGrid
          goal_slug={this.props.goal_slug}
          suggestions={this.state.data}
        />
      </div>
    );
  }
});

export default Suggestion
