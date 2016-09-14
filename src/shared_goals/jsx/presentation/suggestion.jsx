'use strict'

import Goal from 'presentation/goal'
import Review from 'presentation/review'

import React, { PropTypes } from 'react'
import ReactMarkdown from 'react-markdown'

var Suggestion = React.createClass({
  render: function() {}
});

Suggestion.Card = ({ url, suggestion, revision }) => {
  var style = {};
  if (suggestion.image) {
    style.backgroundImage = "url(" + suggestion.image + ")";
  }

  return (
    <a href={url}>
      <div className="suggestion--image" style={style}>
        <div className="suggestion--gradient"></div>
        <span className="suggestion--title">
          <span className="suggestion--title--caption">
            {suggestion.get_type_display} {suggestion.stars}
          </span>
          <h3>{revision.title}</h3>
        </span>
      </div>
    </a>
  );
}

Suggestion.Card.propTypes = {
  url: PropTypes.string.isRequired,
  suggestion: PropTypes.object.isRequired,
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
      <div className="col-md-4 suggestion_CardGridBox" key={suggestion.pk}>
        <Suggestion.Card
          url={"/to/" + goal_slug + "/by/" + suggestion.slug + "/"}
          suggestion={suggestion}
          revision={suggestion.current_revision}
          key={suggestion.pk}
        />
      </div>
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

Suggestion.PageHeader = ({ url, suggestion, revision }) => {
  return (
    <span>
      <div className="row gap--small-above">
        <div className="col-md-4 col-md-offset-4">
          <Suggestion.Card
            url={url}
            suggestion={suggestion}
            revision={revision}
            key={suggestion.pk}
          />
        </div>
      </div>
      <div className="row gap--small-above">
        <div className="col-md-8 col-md-offset-2">
          <h5>Published by {suggestion.owner.name}, {revision.pub_date_display}</h5>
          <ReactMarkdown skipHtml={true} source={revision.description} />
        </div>
      </div>
    </span>
  )
}

export default Suggestion
